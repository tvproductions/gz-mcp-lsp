"""Saved-file generation barriers tested against a controllable process peer."""

from test_session import ProcessFixture

from gz_mcp_lsp.documents import Documents
from gz_mcp_lsp.models import AdapterError
from gz_mcp_lsp.session import Session
from gz_mcp_lsp.workspace import Workspace


class DocumentTests(ProcessFixture):
    """Reuse the executable fixture; inherited lifecycle tests remain intentional."""

    async def test_open_once_and_eviction(self):
        target = self.root / "sample.py"
        target.write_text("x = 1\n")
        async with Session(self.config) as session:
            docs = Documents(Workspace(self.config), session)
            for _ in range(2):
                await docs.prepare(target.as_uri())
                await docs.finish(session.generation)
            self.assertEqual(len(docs.opened), 1)
            await docs.close()
            await session.rpc.request("barrier", {}, timeout=1)
        events = (self.root / "fake-events").read_text()
        self.assertEqual(events.count('"method": "textDocument/didOpen"'), 1)
        self.assertEqual(events.count('"method": "textDocument/didClose"'), 1)

    async def test_unopened_change_create_delete_rename_and_config_restarts(self):
        target = self.root / "sample.py"
        target.write_text("x = 1\n")
        dependency = self.root / "other.py"
        async with Session(self.config) as session:
            docs = Documents(Workspace(self.config), session)
            await docs.prepare(target.as_uri())
            await docs.finish(session.generation)
            for action in [
                lambda: dependency.write_text("x = 2\n"),
                lambda: dependency.write_text("x = 3\n"),
                lambda: dependency.rename(self.root / "renamed.py"),
                lambda: (self.root / "renamed.py").unlink(),
                lambda: (self.root / "ty.toml").write_text(""),
            ]:
                before = session.generation
                previous = session.process
                assert previous is not None
                action()
                await docs.prepare(target.as_uri())
                self.assertNotEqual(before, session.generation)
                self.assertIsNotNone(previous.returncode)
                await docs.finish(session.generation)

    async def test_midquery_change_rejected_and_lock_released(self):
        target = self.root / "sample.py"
        target.write_text("x = 1\n")
        async with Session(self.config) as session:
            docs = Documents(Workspace(self.config), session)
            await docs.prepare(target.as_uri())
            target.write_text("x = 2\n")
            with self.assertRaises(AdapterError) as failure:
                await docs.finish(session.generation)
            self.assertEqual(failure.exception.code, "STALE_DOCUMENT")
            await docs.prepare(target.as_uri())
            await docs.finish(session.generation)

    async def test_incremental_commit_preserves_old_end_and_increments_version(self):
        target = self.root / "sample.py"
        target.write_text('a = "😀"\n')
        workspace = Workspace(self.config)
        async with Session(self.config) as session:
            docs = Documents(workspace, session)
            await docs.prepare(target.as_uri())
            await docs.finish(session.generation)
            target.write_text("a = 2\n")
            await docs.committed([workspace.read(target.as_uri())])
            self.assertEqual(docs.opened[target.as_uri()].version, 2)
            await session.rpc.request("barrier", {}, timeout=1)
            import json

            events = [
                json.loads(line) for line in (self.root / "fake-events").read_text().splitlines()
            ]
            change = next(e for e in events if e.get("method") == "textDocument/didChange")
            self.assertEqual(
                change["params"]["contentChanges"][0]["range"]["end"], {"line": 1, "character": 0}
            )

    async def test_eviction_and_full_change_form(self):
        target = self.root / "sample.py"
        target.write_text("x = 1\n")
        other = self.root / "other.py"
        other.write_text("y = 2\n")
        workspace = Workspace(self.config)
        async with Session(self.config) as session:
            session.capabilities["textDocumentSync"] = {"openClose": True, "change": 1}
            docs = Documents(workspace, session)
            docs.max_open_documents = 1
            for uri in (target.as_uri(), other.as_uri()):
                async with docs.query(uri):
                    pass
            self.assertNotIn(target.as_uri(), docs.opened)
            other.write_text("y = 3\n")
            await docs.committed([workspace.read(other.as_uri())])
            await session.rpc.request("barrier", {}, timeout=1)
            import json

            events = [
                json.loads(line) for line in (self.root / "fake-events").read_text().splitlines()
            ]
            change = next(e for e in events if e.get("method") == "textDocument/didChange")
            self.assertEqual(change["params"]["contentChanges"], [{"text": "y = 3\n"}])
