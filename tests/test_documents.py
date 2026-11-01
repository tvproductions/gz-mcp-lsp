"""Deterministic saved-byte generation ownership."""

import asyncio
import os
import tempfile
import threading
import unittest
from contextlib import suppress
from dataclasses import replace
from pathlib import Path
from typing import Any, cast
from unittest.mock import AsyncMock, patch

from gz_mcp_lsp.config import Config, Limits
from gz_mcp_lsp.models import AdapterError
from gz_mcp_lsp.session import Session
from gz_mcp_lsp.workspace import Workspace


class FakeRpc:
    """Controlled RPC with an observable held request."""

    def __init__(self):
        self.notifications = []
        self.failure = None
        self.started = asyncio.Event()
        self.release = asyncio.Event()

    async def notify(self, method, params):
        self.notifications.append((method, params))

    def fail(self, code, message):
        self.failure = AdapterError(code, message)

    async def request(self, method, params, *, timeout):
        self.started.set()
        await self.release.wait()
        if self.failure:
            raise self.failure
        return {"contents": {"kind": "plaintext", "value": "answer: int"}}


class FakeSession:
    """Restart ordering and live-child accounting."""

    def __init__(self):
        self.rpc = FakeRpc()
        self.state = "READY"
        self.generation = ""
        self.capabilities: dict[str, Any] = {"textDocumentSync": {"openClose": True, "change": 2}}
        self.events = []
        self.live = self.maximum = 1
        self.restart_started = asyncio.Event()

    async def restart(self, generation):
        self.restart_started.set()
        self.events.append("reap")
        self.live -= 1
        self.rpc = FakeRpc()
        self.live += 1
        self.maximum = max(self.maximum, self.live)
        self.events.append("spawn")
        self.generation = generation


class DocumentsTests(unittest.IsolatedAsyncioTestCase):
    """Barriers control readers without readiness sleeps."""

    async def asyncSetUp(self):
        try:
            from gz_mcp_lsp.documents import Documents
        except ImportError as error:
            self.fail(f"Document coordination absent: {error}")
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.a = self.root / "a.py"
        self.b = self.root / "b.py"
        self.a.write_bytes(b"value = 1\n")
        self.b.write_bytes(b"other = 2\n")
        self.config = Config(self.root, self.a, request_timeout_seconds=0.15)
        self.session = FakeSession()
        self.documents = Documents(Workspace(self.config), cast("Session", self.session))
        await self.documents.start()

    async def asyncTearDown(self):
        if hasattr(self, "documents"):
            await self.documents.close()

    async def _generation_value(self):
        async with self.documents.generation() as context:
            return context.generation

    async def test_open_once_close_eviction(self):
        """Cache eviction sends didClose, repeat reads do not reopen."""
        self.documents.workspace.config = replace(self.config, limits=Limits(in_flight_reads=1))
        for _ in range(2):
            async with self.documents.read(self.a.as_uri()):
                pass
        async with self.documents.read(self.b.as_uri()):
            pass
        self.assertEqual(
            [m for m, _ in self.session.rpc.notifications],
            ["textDocument/didOpen", "textDocument/didClose", "textDocument/didOpen"],
        )

    async def test_negotiated_change_versions(self):
        """Exclusive saved commits honor full and incremental sync."""
        for kind in (1, 2):
            self.session.capabilities["textDocumentSync"]["change"] = kind
            async with self.documents.read(self.a.as_uri()):
                pass
            async with self.documents.exclusive():
                self.a.write_bytes(b"changed = 3\n")
                await self.documents.committed([self.documents.workspace.read(self.a.as_uri())])
            change = self.session.rpc.notifications[-1][1]
            self.assertEqual(change["textDocument"]["version"], 2)
            self.assertEqual(change["contentChanges"][0]["text"], "changed = 3\n")
            self.assertEqual("range" in change["contentChanges"][0], kind == 2)
            async with self.documents.read(self.a.as_uri()):
                pass

    async def test_generation_restart_reaps_before_spawn(self):
        """Unopened bytes replace the generation, with one live child."""
        before = await self._generation_value()
        self.b.write_bytes(b"other = 4\n")
        after = await self._generation_value()
        self.assertNotEqual(before, after)
        self.assertEqual(self.session.events, ["reap", "spawn"])
        self.assertLessEqual(self.session.maximum, 1)

    async def test_real_child_generation_restart_reaps_before_spawn(self):
        """The production coordinator reaps actual handles before replacement."""
        import sys

        from gz_mcp_lsp.documents import Documents

        children = []
        peer = Path(__file__).parent / "support/fake_lsp.py"

        async def spawn(*args, **kwargs):
            self.assertTrue(all(child.returncode is not None for child in children))
            child = await asyncio.create_subprocess_exec(sys.executable, str(peer), **kwargs)
            children.append(child)
            return child

        config = replace(self.config, request_timeout_seconds=3)
        session = Session(config, spawn=spawn)
        documents = Documents(Workspace(config), session)
        await documents.start()
        async with session:
            try:
                async with documents.generation() as first:
                    before = first.generation
                self.b.write_bytes(b"other = 10\n")
                async with documents.generation() as second:
                    self.assertNotEqual(before, second.generation)
                self.assertEqual(len(children), 2)
                self.assertIsNotNone(children[0].returncode)
            finally:
                await documents.close()
        self.assertTrue(all(child.returncode is not None for child in children))

    async def test_unopened_change_create_delete_rename(self):
        """Hash bytes, topology, nested configs and ignore policy."""
        for action in ("change", "create", "rename", "delete", "config", "ignore"):
            before = await self._generation_value()
            if action == "change":
                stamp = self.b.stat().st_mtime_ns
                self.b.write_bytes(b"other = 9\n")
                os.utime(self.b, ns=(stamp, stamp))
            elif action == "create":
                (self.root / "new.py").write_bytes(b"x = 1\n")
            elif action == "rename":
                (self.root / "new.py").rename(self.root / "renamed.py")
            elif action == "delete":
                (self.root / "renamed.py").unlink()
            elif action == "config":
                (self.root / "nested").mkdir()
                (self.root / "nested" / "ty.toml").write_bytes(b"[rules]\n")
            else:
                (self.root / ".gitignore").write_bytes(b"nested\n")
            self.assertNotEqual(before, await self._generation_value(), action)

    async def test_midquery_manifest_change_rejected(self):
        """Changed bytes invalidate a completed semantic answer."""
        with self.assertRaises(AdapterError) as raised:
            async with self.documents.read(self.a.as_uri()):
                self.b.write_bytes(b"other = 7\n")
        self.assertEqual(raised.exception.code, "STALE_DOCUMENT")
        self.assertEqual(self.documents.active_count, 0)

    async def test_two_readers_change_restart(self):
        """B invalidates A, then waits for A release before replacing its child."""
        old_rpc = self.session.rpc

        async def reader():
            async with self.documents.read(self.a.as_uri()) as context:
                return await context.rpc.request("hover", {}, timeout=1)

        a = asyncio.create_task(reader())
        await old_rpc.started.wait()
        self.b.write_bytes(b"other = 8\n")
        b = asyncio.create_task(self._generation_value())
        await self.documents.invalidated.wait()
        self.assertFalse(self.session.restart_started.is_set())
        old_rpc.release.set()
        with self.assertRaises(AdapterError) as raised:
            await a
        self.assertEqual(raised.exception.code, "STALE_DOCUMENT")
        await b
        self.assertEqual(self.session.events, ["reap", "spawn"])
        self.assertLessEqual(self.session.maximum, 1)
        self.assertEqual(self.documents.active_count, 0)

    async def test_cancel_releases_read_context(self):
        """Both lease forms release on cancellation."""
        for selected in (False, True):
            entered = asyncio.Event()

            async def reader(selected=selected, entered=entered):
                lease = (
                    self.documents.read(self.a.as_uri())
                    if selected
                    else self.documents.generation()
                )
                async with lease:
                    entered.set()
                    await asyncio.Event().wait()

            task = asyncio.create_task(reader())
            await entered.wait()
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await task
            self.assertEqual(self.documents.active_count, 0)

    async def test_restart_admission_deadline(self):
        """A held old context prevents restart but never waits without a bound."""
        with self.assertRaises(AdapterError) as stale:
            async with self.documents.generation():
                self.b.write_bytes(b"other = 5\n")
                with self.assertRaises(AdapterError) as busy:
                    await self._generation_value()
                self.assertIn(busy.exception.code, {"WORKSPACE_BUSY", "TIMEOUT"})
                self.assertFalse(self.session.restart_started.is_set())
        self.assertEqual(stale.exception.code, "STALE_DOCUMENT")

    async def test_late_reply_cannot_publish_old_generation(self):
        """Even an operation with no pending RPC checks final generation validity."""
        with self.assertRaises(AdapterError) as raised:
            async with self.documents.generation():
                self.b.write_bytes(b"other = 6\n")
                with suppress(AdapterError):
                    await self._generation_value()
        self.assertEqual(raised.exception.code, "STALE_DOCUMENT")

    async def test_generation_lease_without_document(self):
        """Empty workspaces do not require a fabricated document."""
        self.a.unlink()
        self.b.unlink()
        async with self.documents.generation() as context:
            self.assertTrue(context.generation)
            self.assertEqual(self.documents.active_count, 1)
        self.assertEqual(self.session.rpc.notifications, [])

    async def test_document_read_uses_one_lease(self):
        """A document read takes one of the shared admission slots."""
        async with self.documents.read(self.a.as_uri()):
            self.assertEqual(self.documents.active_count, 1)
        self.assertEqual(self.documents.active_count, 0)

    async def test_cancelled_scan_retains_ownership_until_worker_finishes(self):
        """A cancelled thread scan cannot overlap an admitted commit."""
        started = threading.Event()
        released = threading.Event()
        original = self.documents.workspace.semantic_manifest

        def scan():
            started.set()
            if not released.wait(5):
                raise AssertionError("Test scan release was never delivered")
            return original()

        with patch.object(self.documents.workspace, "semantic_manifest", side_effect=scan):
            task = asyncio.create_task(self._generation_value())
            await asyncio.to_thread(started.wait, 5)
            task.cancel()
            turn = asyncio.Event()
            asyncio.get_running_loop().call_soon(turn.set)
            await turn.wait()
            try:
                self.assertFalse(task.done(), "Thread outlived its admission owner")
            finally:
                released.set()
                with self.assertRaises(asyncio.CancelledError):
                    await task
        self.assertEqual(self.documents.active_count, 0)

    async def test_unreconciled_source_scope_fails_closed(self):
        """External source roots and hidden mutable exclusions cannot claim freshness."""
        config_path = self.root / "ty.toml"
        config_path.write_bytes(b'[environment]\nextra-paths = ["../external"]\n')
        with self.assertRaises(AdapterError) as raised:
            await self._generation_value()
        self.assertEqual(raised.exception.code, "UNSUPPORTED")
        config_path.write_bytes(b'[src]\ninclude = ["../external/**"]\n')
        with self.assertRaises(AdapterError) as raised:
            await self._generation_value()
        self.assertEqual(raised.exception.code, "UNSUPPORTED")
        config_path.unlink()
        self.documents.workspace.config = replace(self.config, exclusions=("hidden",))
        with self.assertRaises(AdapterError) as raised:
            await self._generation_value()
        self.assertEqual(raised.exception.code, "UNSUPPORTED")

    async def test_same_manifest_restart_still_changes_generation(self):
        """A new transport never reuses resultIds from an unchanged manifest."""
        before = await self._generation_value()
        note = self.root / "note.txt"
        async with self.documents.exclusive():
            note.write_bytes(b"saved outside Python indexing\n")
            await self.documents.committed([self.documents.workspace.read(note.as_uri())])
        after = await self._generation_value()
        self.assertNotEqual(before, after)

    async def test_untracked_semantic_document_is_unsupported(self):
        """Semantic leases never pretend unscanned file bytes share the manifest."""
        note = self.root / "note.txt"
        note.write_bytes(b"answer = 1\n")
        with self.assertRaises(AdapterError) as raised:
            async with self.documents.read(note.as_uri()):
                pass
        self.assertEqual(raised.exception.code, "UNSUPPORTED")

    async def test_failed_replacement_is_not_retried_by_later_reads(self):
        """A failed new child is not hidden behind the old invalidation marker."""

        async def fail(generation):
            self.session.state = "FAILED"
            raise AdapterError("SERVER_EXITED", "Synthetic replacement failed")

        self.session.restart = AsyncMock(side_effect=fail)
        self.b.write_bytes(b"other = 11\n")
        for _ in range(2):
            with self.assertRaises(AdapterError) as raised:
                await self._generation_value()
            self.assertEqual(raised.exception.code, "SERVER_EXITED")
        self.assertEqual(self.session.restart.await_count, 1)

    async def test_failed_child_is_not_restarted(self):
        """Unexpected death remains a source-independent failure."""
        self.session.state = "FAILED"
        with self.assertRaises(AdapterError) as raised:
            await self._generation_value()
        self.assertEqual(raised.exception.code, "SERVER_EXITED")
        self.assertEqual(self.session.events, [])
        self.b.write_bytes(b"changed_after_exit = 1\n")
        with self.assertRaises(AdapterError) as changed:
            await self._generation_value()
        self.assertEqual(changed.exception.code, "SERVER_EXITED")
        self.assertEqual(self.session.events, [])

    async def test_exclusive_does_not_expire_after_drain(self):
        """The drain deadline never interrupts a held transaction body."""
        async with self.documents.exclusive():
            self.documents.workspace.config = replace(self.config, request_timeout_seconds=0.001)
            # An event-loop timer is a deadline negative control, not a readiness sleep.
            event = asyncio.Event()
            asyncio.get_running_loop().call_later(0.2, event.set)
            await event.wait()

    async def test_exclusive_drain_and_admission(self):
        """Commit exclusion blocks new reads until release."""
        async with self.documents.exclusive():
            with self.assertRaises(AdapterError) as raised:
                await self._generation_value()
            self.assertEqual(raised.exception.code, "WORKSPACE_BUSY")
        self.assertEqual(self.documents.active_count, 0)
