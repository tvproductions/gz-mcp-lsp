"""Saved-disk synchronization with serialized, observable workspace generations."""

import asyncio
from collections import OrderedDict
from collections.abc import AsyncGenerator, Sequence
from contextlib import asynccontextmanager
from dataclasses import replace

from gz_mcp_lsp.models import AdapterError, Json, Snapshot
from gz_mcp_lsp.ports import SessionPort
from gz_mcp_lsp.workspace import Workspace


def end_position(data: bytes) -> dict[str, Json]:
    """Return the UTF-16 EOF coordinate, retaining the final empty line."""
    lines = data.decode("utf-8").split("\n")
    return {"line": len(lines) - 1, "character": len(lines[-1].encode("utf-16-le")) // 2}


class Documents:
    """Hold one operation lease through its post-query generation check."""

    def __init__(self, workspace: Workspace, session: SessionPort):
        self.workspace = workspace
        self.session = session
        self.lock = asyncio.Lock()
        self.max_open_documents = 128
        self.opened: OrderedDict[str, Snapshot] = OrderedDict()

    async def prepare(self, uri: str | None) -> Snapshot | None:
        """Reconcile saved scope and open only the requested document once."""
        await self.lock.acquire()
        try:
            manifest = await asyncio.to_thread(self.workspace.manifest)
            if self.session.generation and manifest != self.session.generation:
                await self.close()
                await self.session.restart(manifest)
                self.opened.clear()
            self.session.generation = manifest
            if uri is None:
                return None
            snapshot = await asyncio.to_thread(self.workspace.read, uri)
            if snapshot.uri not in self.opened:
                sync = self.session.capabilities.get("textDocumentSync")
                if isinstance(sync, dict) and not sync.get("openClose", False):
                    raise AdapterError("UNSUPPORTED", "Server cannot synchronize document opens")
                if not isinstance(sync, (int, dict)) or sync is False or sync == 0:
                    raise AdapterError("UNSUPPORTED", "Missing document synchronization capability")
                if len(self.opened) >= self.max_open_documents:
                    evicted, _ = self.opened.popitem(last=False)
                    await self.session.rpc.notify(
                        "textDocument/didClose", {"textDocument": {"uri": evicted}}
                    )
                await self.session.rpc.notify(
                    "textDocument/didOpen",
                    {
                        "textDocument": {
                            "uri": snapshot.uri,
                            "languageId": "python",
                            "version": 1,
                            "text": snapshot.data.decode("utf-8"),
                        }
                    },
                )
                self.opened[snapshot.uri] = snapshot
            else:
                self.opened.move_to_end(snapshot.uri)
                snapshot = replace(snapshot, version=self.opened[snapshot.uri].version)
            return snapshot
        except BaseException:
            self.lock.release()
            raise

    async def finish(self, generation: str) -> None:
        """Reject stale query output, releasing the operation lease even on failure."""
        try:
            manifest = await asyncio.to_thread(self.workspace.manifest)
            if generation != self.session.generation or manifest != generation:
                raise AdapterError("STALE_DOCUMENT", "Workspace changed during the request", True)
        finally:
            self.lock.release()

    @asynccontextmanager
    async def query(self, uri: str | None) -> AsyncGenerator[Snapshot | None]:
        """Own lease cleanup for failed/cancelled operations as well as successful reads."""
        snapshot = await self.prepare(uri)
        generation = self.session.generation
        try:
            yield snapshot
        except BaseException:
            self.lock.release()
            raise
        else:
            await self.finish(generation)

    async def committed(self, snapshots: Sequence[Snapshot]) -> None:
        """Honor negotiated change form; the next prepare still enforces a restart."""
        sync = self.session.capabilities.get("textDocumentSync")
        kind = sync.get("change") if isinstance(sync, dict) else sync
        for snapshot in snapshots:
            previous = self.opened.get(snapshot.uri)
            if previous is None:
                continue
            if kind not in (1, 2):
                raise AdapterError("UNSUPPORTED", "Server cannot synchronize changes")
            version = previous.version + 1
            change: dict[str, Json] = {"text": snapshot.data.decode("utf-8")}
            if kind == 2:
                change["range"] = {
                    "start": {"line": 0, "character": 0},
                    "end": end_position(previous.data),
                }
            await self.session.rpc.notify(
                "textDocument/didChange",
                {
                    "textDocument": {"uri": snapshot.uri, "version": version},
                    "contentChanges": [change],
                },
            )
            self.opened[snapshot.uri] = replace(snapshot, version=version)

    async def close(self) -> None:
        """Close tracked documents before generation shutdown when transport remains live."""
        for uri in list(self.opened):
            await self.session.rpc.notify("textDocument/didClose", {"textDocument": {"uri": uri}})
            del self.opened[uri]
