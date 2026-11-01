"""Bounded generation leases and saved-file synchronization for one ty session."""

import asyncio
import re
from collections import OrderedDict
from collections.abc import AsyncGenerator, Callable, Sequence
from contextlib import asynccontextmanager, suppress
from dataclasses import dataclass, replace

from gz_mcp_lsp.lsp_transport import RpcClient
from gz_mcp_lsp.models import AdapterError, Json, Snapshot
from gz_mcp_lsp.session import Session
from gz_mcp_lsp.workspace import Workspace


@dataclass(frozen=True, slots=True)
class GenerationContext:
    """Pin a single immutable generation and transport for a whole operation."""

    generation: str
    rpc: RpcClient


@dataclass(frozen=True, slots=True)
class ReadContext:
    """Add exact saved bytes without acquiring a second admission slot."""

    snapshot: Snapshot
    generation: str
    rpc: RpcClient


class Documents:
    """Serialize reconciliation while allowing bounded concurrent semantic readers."""

    def __init__(self, workspace: Workspace, session: Session):
        self.workspace = workspace
        self.session = session
        self.invalidated = asyncio.Event()
        self._admission = asyncio.Lock()
        self._open_lock = asyncio.Lock()
        self._drained = asyncio.Condition()
        self._active = 0
        self._exclusive = False
        self._closed = False
        self._failed_transition = False
        self._generation = ""
        self._opened: OrderedDict[str, Snapshot] = OrderedDict()
        self._users: dict[str, int] = {}

    @property
    def active_count(self) -> int:
        """Expose bounded ownership for lifecycle evidence."""

        return self._active

    async def start(self) -> None:
        """Seed scope before starting the child, without choosing a document."""

        self._generation = await self._manifest()
        self.session.generation = self._generation

    async def _manifest(self) -> str:
        return await _owned_io(self.workspace.semantic_manifest)

    def _invalidate(self) -> None:
        if not self.invalidated.is_set():
            self.invalidated.set()
            self.session.rpc.fail("STALE_DOCUMENT", "Workspace generation changed")

    async def _reconcile(self) -> None:
        if self._failed_transition or (
            self.session.state != "READY" and not self.invalidated.is_set()
        ):
            raise AdapterError("SERVER_EXITED", "Language-server session exited unexpectedly")
        manifest = await self._manifest()
        if manifest != self._generation:
            self._invalidate()
        if self.invalidated.is_set():
            async with self._drained:
                await self._drained.wait_for(lambda: self._active == 0)
            try:
                await self.session.restart(manifest)
            except BaseException:
                self._failed_transition = True
                raise
            self._opened.clear()
            self._users.clear()
            self._generation = manifest
            self.invalidated.clear()
        elif self.session.state != "READY":
            raise AdapterError("SERVER_EXITED", "Language-server session is not ready")

    async def _acquire(self) -> GenerationContext:
        if self._closed or self._exclusive:
            raise AdapterError("WORKSPACE_BUSY", "Workspace admission is closed")
        async with self._admission:
            if self._closed or self._exclusive:
                raise AdapterError("WORKSPACE_BUSY", "Workspace admission is closed")
            await self._reconcile()
            if self._active >= self.workspace.config.limits.in_flight_reads:
                raise AdapterError("WORKSPACE_BUSY", "Semantic reader limit reached", True)
            self._active += 1
            return GenerationContext(self._generation, self.session.rpc)

    async def _validate(self, context: GenerationContext) -> None:
        if context.generation != self._generation or self.invalidated.is_set():
            raise AdapterError("STALE_DOCUMENT", "Semantic result belongs to an old generation")
        if await self._manifest() != context.generation:
            self._invalidate()
            raise AdapterError("STALE_DOCUMENT", "Workspace changed during the semantic operation")
        if self.session.state != "READY":
            raise AdapterError(
                "SERVER_EXITED", "Language-server session exited during the operation"
            )

    @asynccontextmanager
    async def generation(self) -> AsyncGenerator[GenerationContext]:
        """Pin admission through RPCs, extraction and final manifest validation."""

        context = None
        try:
            async with asyncio.timeout(self.workspace.config.request_timeout_seconds):
                context = await self._acquire()
                try:
                    yield context
                    await self._validate(context)
                finally:
                    # Release never waits for the restart that this release enables.
                    async with self._drained:
                        self._active -= 1
                        self._drained.notify_all()
        except TimeoutError as error:
            if context is not None and self.invalidated.is_set():
                raise AdapterError(
                    "STALE_DOCUMENT", "Generation invalidated during the operation"
                ) from error
            raise AdapterError(
                "TIMEOUT", "Semantic operation exceeded its request budget", True
            ) from error

    @asynccontextmanager
    async def read(self, uri: str) -> AsyncGenerator[ReadContext]:
        """Compose one generation lease with serialized validated snapshot/open."""

        async with self.generation() as context:
            key = await _owned_io(self.workspace.canonical_uri, uri)
            async with self._open_lock:
                snapshot = await _owned_io(self.workspace.read, uri)
                await self._open(key, snapshot, context.rpc)
                self._users[key] = self._users.get(key, 0) + 1
            try:
                await self._validate(context)
                yield ReadContext(snapshot, context.generation, context.rpc)
            finally:
                self._users[key] -= 1

    async def _open(self, key: str, snapshot: Snapshot, rpc: RpcClient) -> None:
        if key in self._opened:
            previous = self._opened[key]
            if previous.sha256 != snapshot.sha256 or previous.identity != snapshot.identity:
                self._invalidate()
                raise AdapterError(
                    "STALE_DOCUMENT", "Opened document changed before synchronization"
                )
            self._opened.move_to_end(key)
            return
        if len(self._opened) >= self.workspace.config.limits.in_flight_reads:
            victim = next((uri for uri in self._opened if not self._users.get(uri)), None)
            if victim is None:
                raise AdapterError("WORKSPACE_BUSY", "All synchronized document slots are in use")
            await rpc.notify("textDocument/didClose", {"textDocument": {"uri": victim}})
            del self._opened[victim]
        if not self._sync_open_close():
            raise AdapterError(
                "UNSUPPORTED", "Language server does not support document open/close"
            )
        await rpc.notify(
            "textDocument/didOpen",
            {
                "textDocument": {
                    "uri": key,
                    "languageId": "python",
                    "version": 1,
                    "text": snapshot.data.decode("utf-8"),
                }
            },
        )
        self._opened[key] = snapshot

    def _sync_open_close(self) -> bool:
        sync = self.session.capabilities.get("textDocumentSync")
        return (type(sync) is int and sync in (1, 2)) or (
            isinstance(sync, dict) and sync.get("openClose") is True
        )

    @asynccontextmanager
    async def exclusive(self) -> AsyncGenerator[None]:
        """Close admission and drain old readers before any mutation preflight."""

        if self._exclusive or self._closed:
            raise AdapterError("WORKSPACE_BUSY", "Workspace is already exclusively owned")
        try:
            async with asyncio.timeout(self.workspace.config.request_timeout_seconds):
                await self._admission.acquire()
                self._exclusive = True
                try:
                    async with self._drained:
                        await self._drained.wait_for(lambda: self._active == 0)
                except BaseException:
                    self._exclusive = False
                    self._admission.release()
                    raise
        except TimeoutError as error:
            raise AdapterError(
                "WORKSPACE_BUSY", "Unable to drain workspace readers", True
            ) from error
        try:
            yield
        finally:
            self._exclusive = False
            self._admission.release()

    async def committed(self, snapshots: Sequence[Snapshot]) -> None:
        """Synchronize saved changes under exclusive authority; invalidate for next read."""

        if not self._exclusive or self._active:
            raise AdapterError("WORKSPACE_BUSY", "Saved changes require exclusive ownership")
        try:
            for snapshot in snapshots:
                key = await _owned_io(self.workspace.canonical_uri, snapshot.uri)
                previous = self._opened.get(key)
                if previous is None:
                    continue
                sync = self.session.capabilities.get("textDocumentSync")
                kind = sync.get("change") if isinstance(sync, dict) else sync
                change: dict[str, Json] = {"text": snapshot.data.decode("utf-8")}
                if kind == 2:
                    change["range"] = {"start": {"line": 0, "character": 0}, "end": _end(previous)}
                elif kind != 1:
                    raise AdapterError(
                        "UNSUPPORTED", "Language server does not support saved changes"
                    )
                version = previous.version + 1
                await self.session.rpc.notify(
                    "textDocument/didChange",
                    {
                        "textDocument": {"uri": key, "version": version},
                        "contentChanges": [change],
                    },
                )
                self._opened[key] = replace(snapshot, version=version)
        finally:
            self._invalidate()

    async def close(self) -> None:
        """Close the synchronized set before the Session owner shuts down the child."""

        self._closed = True
        async with self._open_lock:
            for uri in self._opened:
                with suppress(AdapterError, TimeoutError):
                    async with asyncio.timeout(self.workspace.config.shutdown_timeout_seconds):
                        await self.session.rpc.notify(
                            "textDocument/didClose", {"textDocument": {"uri": uri}}
                        )
            self._opened.clear()


async def _owned_io[T](call: Callable[..., T], *args) -> T:
    """Retain the owning lease until its bounded synchronous IO has actually ended."""

    task = asyncio.create_task(asyncio.to_thread(call, *args))
    cancelled = False
    while not task.done():
        try:
            await asyncio.shield(task)
        except asyncio.CancelledError:
            cancelled = True
    if cancelled:
        with suppress(Exception):
            task.result()
        raise asyncio.CancelledError
    return task.result()


def _end(snapshot: Snapshot) -> dict[str, Json]:
    text = snapshot.data.decode("utf-8")
    lines = re.split(r"\r\n|\r|\n", text)
    return {"line": len(lines) - 1, "character": len(lines[-1].encode("utf-16-le")) // 2}
