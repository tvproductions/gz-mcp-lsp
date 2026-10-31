"""Single-process ty lifecycle; transport owns bytes, this module owns resources."""

import asyncio
import os
from contextlib import suppress

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.lsp_transport import RpcClient
from gz_mcp_lsp.models import AdapterError, Json


class Session:
    """Initialize exactly once per child and reap before any generation restart."""

    def __init__(self, config: Config):
        self.config = config
        self.capabilities: dict[str, Json] = {}
        self.generation = ""
        self.state = "NEW"
        self.process: asyncio.subprocess.Process | None = None
        self._rpc: RpcClient | None = None
        self._stderr: asyncio.Task | None = None
        self._watcher: asyncio.Task | None = None
        self._stop_lock = asyncio.Lock()
        self.stderr_tail = b""

    @property
    def rpc(self) -> RpcClient:
        """Reject access before initialization or after terminal shutdown."""
        if self._rpc is None:
            raise AdapterError("SERVER_EXITED", "Language-server session is unavailable")
        return self._rpc

    async def _configuration(self, params: Json) -> Json:
        items = params.get("items") if isinstance(params, dict) else None
        if not isinstance(items, list):
            raise AdapterError("PROTOCOL_ERROR", "Invalid configuration callback")
        return [None for _ in items]

    async def _deny_edit(self, params: Json) -> Json:
        return {"applied": False, "failureReason": "Unsolicited edits are disabled"}

    async def _folders(self, params: Json) -> Json:
        return [
            {"uri": self.config.workspace_root.as_uri(), "name": self.config.workspace_root.name}
        ]

    async def _drain_stderr(self) -> None:
        assert self.process is not None and self.process.stderr is not None
        try:
            while chunk := await self.process.stderr.read(4096):
                self.stderr_tail = (self.stderr_tail + chunk)[-4096:]
        except OSError:
            self.rpc._fail(AdapterError("SERVER_EXITED", "Language-server stderr stream failed"))

    async def _watch(self) -> None:
        """Reap on process death or terminal transport failure, without a host retry."""
        process, rpc = self.process, self._rpc
        if process is None or rpc is None:
            return
        exited = asyncio.create_task(process.wait())
        try:
            await asyncio.wait((exited, rpc.failure), return_when=asyncio.FIRST_COMPLETED)
            if self.state not in ("STOPPING", "CLOSED"):
                self.state = "FAILED"
                rpc._fail(AdapterError("SERVER_EXITED", "Language-server session failed"))
                await self.close()
        finally:
            exited.cancel()
            await asyncio.gather(exited, return_exceptions=True)

    async def _start(self) -> None:
        self.state = "STARTING"
        self.stderr_tail = b""
        try:
            self.process = await asyncio.create_subprocess_exec(
                str(self.config.ty_executable),
                "server",
                cwd=self.config.workspace_root,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                limit=self.config.limits.max_header_bytes + 1,
            )
            assert self.process.stdout is not None and self.process.stdin is not None
            self._rpc = RpcClient(self.process.stdout, self.process.stdin, self.config)
            self.rpc.set_handler("workspace/configuration", self._configuration)
            self.rpc.set_handler("workspace/applyEdit", self._deny_edit)
            self.rpc.set_handler("workspace/workspaceFolders", self._folders)
            self._stderr = asyncio.create_task(self._drain_stderr(), name="gz-ty-stderr")
            self._watcher = asyncio.create_task(self._watch(), name="gz-ty-process")
            self.state = "INITIALIZING"
            result = await self.rpc.request(
                "initialize",
                {
                    "processId": os.getpid(),
                    "rootUri": self.config.workspace_root.as_uri(),
                    "workspaceFolders": await self._folders(None),
                    "capabilities": {
                        "general": {"positionEncodings": ["utf-16"]},
                        "workspace": {
                            "configuration": True,
                            "workspaceFolders": True,
                            "workspaceEdit": {"documentChanges": True},
                        },
                        "textDocument": {
                            "synchronization": {"didSave": False, "dynamicRegistration": False},
                            "definition": {"linkSupport": True},
                            "implementation": {"linkSupport": True},
                            "documentSymbol": {"hierarchicalDocumentSymbolSupport": True},
                            "diagnostic": {"relatedDocumentSupport": True},
                            "rename": {"prepareSupport": True},
                        },
                    },
                },
                timeout=self.config.limits.initialize_seconds,
            )
            capabilities = result.get("capabilities") if isinstance(result, dict) else None
            if not isinstance(capabilities, dict):
                raise AdapterError("PROTOCOL_ERROR", "Missing server capabilities")
            self.capabilities = capabilities
            if self.capabilities.get("positionEncoding", "utf-16") != "utf-16":
                raise AdapterError("UNSUPPORTED", "Server did not negotiate UTF-16 positions")
            await self.rpc.notify("initialized", {})
            self.state = "READY"
        except BaseException as error:
            await asyncio.shield(self.close())
            if isinstance(error, OSError):
                raise AdapterError(
                    "SERVER_EXITED", "Cannot launch configured language server"
                ) from error
            raise

    async def __aenter__(self):
        """Start a new session; repeated entry is a caller error."""
        if self.state != "NEW":
            raise AdapterError("INVALID_INPUT", "Session already started")
        await self._start()
        return self

    async def __aexit__(self, *exc):
        """Reap even when the MCP host disconnects or cancels its lifespan."""
        cleanup = asyncio.create_task(self.close())
        try:
            await asyncio.shield(cleanup)
        except asyncio.CancelledError:
            await cleanup
            raise

    async def restart(self, generation: str) -> None:
        """No overlap: old process is reaped before a replacement is spawned."""
        await self.close()
        self.generation = generation
        await self._start()

    async def _reap(self) -> None:
        assert self.process is not None
        try:
            async with asyncio.timeout(self.config.limits.escalation_seconds):
                await self.process.wait()
                return
        except TimeoutError:
            pass
        for signal in (self.process.terminate, self.process.kill):
            with suppress(ProcessLookupError):
                signal()
            try:
                async with asyncio.timeout(self.config.limits.escalation_seconds):
                    await self.process.wait()
                    return
            except TimeoutError:
                continue
        raise AdapterError("SERVER_EXITED", "Language-server process could not be reaped")

    async def close(self) -> None:
        """Idempotent bounded shutdown, exit, pipe close, escalation and reaping."""
        async with self._stop_lock:
            if self.state == "CLOSED":
                return
            ready = self.state == "READY"
            self.state = "STOPPING"
            try:
                if self._rpc is not None:
                    if ready:
                        with suppress(AdapterError):
                            await self.rpc.request(
                                "shutdown", None, timeout=self.config.limits.shutdown_seconds
                            )
                    with suppress(AdapterError):
                        await self.rpc.notify("exit", None)
                    await self.rpc.close()
                if self.process is not None:
                    await self._reap()
            finally:
                tasks = [
                    task
                    for task in (self._stderr, self._watcher)
                    if task is not None and task is not asyncio.current_task()
                ]
                for task in tasks:
                    task.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
                self._rpc = None
                self.state = "CLOSED"
