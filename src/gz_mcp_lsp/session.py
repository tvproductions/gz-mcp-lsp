"""One ty child with explicit initialization, failure supervision and bounded cleanup."""

import asyncio
import os
import subprocess
from collections.abc import Awaitable, Callable
from contextlib import suppress
from typing import cast

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.lsp_transport import RpcClient
from gz_mcp_lsp.models import AdapterError, Json

type Spawn = Callable[..., Awaitable[asyncio.subprocess.Process]]


class Session:
    """Own the child, transport and diagnostic drain; never replay semantic calls."""

    def __init__(self, config: Config, *, spawn: Spawn = asyncio.create_subprocess_exec):
        self.config = config
        self.spawn = spawn
        self.state = "NEW"
        self.capabilities: dict[str, Json] = {}
        self.generation = ""
        self.stderr_tail = b""
        self._process: asyncio.subprocess.Process | None = None
        self._rpc: RpcClient | None = None
        self._stderr_task: asyncio.Task[None] | None = None
        self._monitor: asyncio.Task[None] | None = None
        self._close_lock = asyncio.Lock()
        self._closed = asyncio.Event()

    @property
    def rpc(self) -> RpcClient:
        """Return the owned transport once allocated, including during initialize."""
        if self._rpc is None:
            raise AdapterError("SERVER_EXITED", "Session transport is not available")
        return self._rpc

    @property
    def process(self) -> asyncio.subprocess.Process:
        """Expose the owned child handle for lifecycle evidence."""
        if self._process is None:
            raise AdapterError("SERVER_EXITED", "Session child is not available")
        return self._process

    async def __aenter__(self) -> Session:
        if self.state != "NEW":
            raise AdapterError("SERVER_EXITED", "Session has already started")
        self.state = "STARTING"
        try:
            self._process = await self._spawn_child()
            if self.process.stdout is None or self.process.stdin is None:
                raise AdapterError("SERVER_EXITED", "Unable to allocate language-server pipes")
            self._rpc = RpcClient(self.process.stdout, self.process.stdin, self.config)
            self.rpc.set_handler("workspace/configuration", self._configuration)
            self.rpc.set_handler("workspace/applyEdit", self._deny_edit)
            self.rpc.start()
            self._stderr_task = asyncio.create_task(self._drain_stderr())
            self._monitor = asyncio.create_task(self._watch())
            self.state = "INITIALIZING"
            result = await self.rpc.request(
                "initialize",
                self._initialize_params(),
                timeout=self.config.initialize_timeout_seconds,
            )
            self.capabilities = _capabilities(result)
            await self.rpc.notify("initialized", {})
            self.state = "READY"
            return self
        except BaseException:
            self.state = "FAILED"
            await self._shielded_close()
            raise

    async def __aexit__(self, *args) -> None:
        await self._shielded_close()

    async def _spawn_child(self) -> asyncio.subprocess.Process:
        try:
            return await self.spawn(
                str(self.config.ty_executable),
                "server",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.config.workspace_root),
                limit=self.config.limits.header_bytes,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            )
        except OSError as error:
            raise AdapterError(
                "SERVER_EXITED", "Unable to launch the provisioned ty executable"
            ) from error

    async def _shielded_close(self) -> None:
        task = asyncio.create_task(self.close())
        cancelled = False
        while not task.done():
            try:
                await asyncio.shield(task)
            except asyncio.CancelledError:
                cancelled = True
        task.result()
        if cancelled:
            raise asyncio.CancelledError

    def _initialize_params(self) -> dict[str, Json]:
        return {
            "processId": os.getpid(),
            "rootUri": self.config.workspace_root.as_uri(),
            "workspaceFolders": [
                {
                    "uri": self.config.workspace_root.as_uri(),
                    "name": self.config.workspace_root.name,
                }
            ],
            "clientInfo": {"name": "gz-mcp-lsp", "version": "0.1.0"},
            "capabilities": {
                "general": {"positionEncodings": ["utf-16"]},
                "workspace": {
                    "configuration": True,
                    "applyEdit": False,
                    "symbol": {"resolveSupport": {"properties": ["location.range"]}},
                    "workspaceEdit": {
                        "documentChanges": True,
                        "resourceOperations": [],
                        "changeAnnotationSupport": {"groupsOnLabel": False},
                    },
                },
                "textDocument": {
                    "synchronization": {"dynamicRegistration": False},
                    "definition": {"linkSupport": True},
                    "implementation": {"linkSupport": True},
                    "rename": {"prepareSupport": True},
                    "diagnostic": {"dynamicRegistration": False, "relatedDocumentSupport": True},
                    "publishDiagnostics": {
                        "relatedInformation": True,
                        "tagSupport": {"valueSet": [1, 2]},
                        "codeDescriptionSupport": True,
                        "dataSupport": False,
                    },
                    "documentSymbol": {"hierarchicalDocumentSymbolSupport": True},
                },
            },
            "initializationOptions": {
                "untrustedWorkspace": True,
                "experimental": {"useUv": "off"},
                "logLevel": "warn",
            },
            "trace": "off",
        }

    async def _configuration(self, params: Json) -> Json:
        if not isinstance(params, dict) or not isinstance(params.get("items"), list):
            raise AdapterError("PROTOCOL_ERROR", "Invalid configuration callback")
        return [{} for _ in cast("list[Json]", params["items"])]

    async def _deny_edit(self, params: Json) -> Json:
        return {"applied": False, "failureReason": "Unsolicited edits are disabled"}

    async def _drain_stderr(self) -> None:
        if self.process.stderr is None:
            self.rpc.fail("SERVER_EXITED", "Language-server stderr is unavailable")
            return
        try:
            while chunk := await self.process.stderr.read(4096):
                self.stderr_tail = (self.stderr_tail + chunk)[-65536:]
        except OSError:
            self.rpc.fail("SERVER_EXITED", "Language-server stderr failed")

    async def _watch(self) -> None:
        child = asyncio.create_task(self.process.wait())
        wire = asyncio.create_task(self.rpc.wait_failure())
        try:
            done, _ = await asyncio.wait({child, wire}, return_when=asyncio.FIRST_COMPLETED)
            if self.state not in {"STOPPING", "CLOSED"}:
                self.state = "FAILED"
                failure = (
                    wire.result()
                    if wire in done
                    else AdapterError("SERVER_EXITED", "Language-server child exited")
                )
                self.rpc.fail(failure.code, failure.message)
                await self.close()
        finally:
            child.cancel()
            wire.cancel()
            await asyncio.gather(child, wire, return_exceptions=True)

    async def wait_closed(self) -> None:
        """Wait for observed cleanup, not an arbitrary readiness/termination sleep."""
        await self._closed.wait()

    async def close(self) -> None:
        """Serialize duplicate cleanup and retain failure state after reaping."""
        async with self._close_lock:
            if self._closed.is_set():
                return
            failed = self.state == "FAILED"
            graceful = self.state == "READY"
            self.state = "STOPPING"
            if self._monitor is not None and self._monitor is not asyncio.current_task():
                self._monitor.cancel()
                await asyncio.gather(self._monitor, return_exceptions=True)
            try:
                if self._process is not None:
                    await self._stop_child(graceful)
            except BaseException:
                failed = True
                raise
            finally:
                try:
                    if self._rpc is not None:
                        await self.rpc.close()
                finally:
                    if self._stderr_task is not None:
                        self._stderr_task.cancel()
                        await asyncio.gather(self._stderr_task, return_exceptions=True)
                    self.state = "FAILED" if failed else "CLOSED"
                    self._closed.set()

    async def _stop_child(self, graceful: bool) -> None:
        if self.process.returncode is not None:
            return
        try:
            async with asyncio.timeout(self.config.shutdown_timeout_seconds):
                if graceful and self._rpc is not None:
                    with suppress(AdapterError):
                        await self.rpc.request(
                            "shutdown", None, timeout=self.config.shutdown_timeout_seconds
                        )
                        await self.rpc.notify("exit", None)
                if self.process.stdin is not None:
                    self.process.stdin.close()
                await self.process.wait()
                return
        except TimeoutError:
            pass
        with suppress(ProcessLookupError):
            self.process.terminate()
        if await self._reaped_within(self.config.kill_timeout_seconds / 2):
            return
        with suppress(ProcessLookupError):
            self.process.kill()
        if not await self._reaped_within(self.config.kill_timeout_seconds / 2):
            raise AdapterError("SERVER_EXITED", "Unable to reap language-server child")

    async def _reaped_within(self, seconds: float) -> bool:
        try:
            async with asyncio.timeout(seconds):
                await self.process.wait()
                return True
        except TimeoutError:
            return False

    async def restart(self, generation: str) -> None:
        """A generation owner must drain admission before replacing this child."""
        await self.close()
        if self._process is not None and self.process.returncode is None:
            raise AdapterError(
                "SERVER_EXITED", "Previous language-server child has not been reaped"
            )
        self.state = "NEW"
        self._closed.clear()
        self.capabilities = {}
        self._rpc = None
        self._process = None
        self._monitor = None
        self._stderr_task = None
        self.generation = generation
        await self.__aenter__()


def _capabilities(result: Json) -> dict[str, Json]:
    if not isinstance(result, dict) or not isinstance(result.get("capabilities"), dict):
        raise AdapterError("PROTOCOL_ERROR", "Invalid initialize result")
    capabilities = cast("dict[str, Json]", result["capabilities"])
    if capabilities.get("positionEncoding", "utf-16") != "utf-16":
        raise AdapterError("UNSUPPORTED", "Language server did not select UTF-16")
    return capabilities
