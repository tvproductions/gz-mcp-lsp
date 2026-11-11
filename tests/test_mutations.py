"""Mutation admission, retained previews and coordinated durable outcomes."""

import asyncio
import hashlib
import tempfile
import threading
import unittest
from dataclasses import replace
from pathlib import Path
from typing import Any, cast
from unittest.mock import patch

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.documents import Documents
from gz_mcp_lsp.filesystem import Transactions
from gz_mcp_lsp.models import AdapterError, Position, Range, TextEdit
from gz_mcp_lsp.session import Session
from gz_mcp_lsp.workspace import Workspace
from tests.test_documents import FakeRpc, FakeSession


class RenameRpc(FakeRpc):
    def __init__(self):
        super().__init__()
        self.requests = []
        self.prepare: Any = {
            "start": {"line": 0, "character": 0},
            "end": {"line": 0, "character": 5},
        }
        self.edit = None

    async def request(self, method, params, *, timeout):
        self.requests.append((method, params))
        return self.prepare if method.endswith("/prepareRename") else self.edit


class MemoryTransactions:
    """Observe the service's ordering; syscall safety is tested by the real adapter."""

    def __init__(self):
        self.paths = {}
        self.receipts = {}
        self.calls = []
        self.started = threading.Event()
        self.release = threading.Event()
        self.release.set()
        self.recovery = []
        self.error = None

    def recover(self):
        self.calls.append("recover")
        if self.error:
            raise self.error
        return self.recovery

    def receipt(self, plan_id):
        return self.receipts.get(plan_id)

    def apply(self, plan):
        self.calls.append("apply")
        self.started.set()
        if not self.release.wait(10):
            raise AssertionError("Commit barrier was not released")
        for file in plan.files:
            self.paths[file.uri].write_bytes(file.after)
        receipt = {"schema_version": 1, "plan_id": plan.plan_id, "status": "committed", "files": []}
        self.receipts[plan.plan_id] = receipt
        return receipt


async def until(predicate):
    async with asyncio.timeout(10):
        while not predicate():
            await asyncio.sleep(0)


class MutationTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        try:
            from gz_mcp_lsp.mutations import Mutations
        except ImportError as error:
            self.fail(f"Mutation service absent: {error}")
        self.platform_patch = patch(
            "gz_mcp_lsp.mutations.write_platform_supported", return_value=True
        )
        self.platform_patch.start()
        self.addCleanup(self.platform_patch.stop)
        temporary = tempfile.TemporaryDirectory(prefix="gz-mutation-unit-", dir=Path.home())
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name).resolve()
        self.root = self.base / "workspace"
        self.root.mkdir()
        self.a = self.root / "a.py"
        self.b = self.root / "b.py"
        self.a.write_bytes(b"value = 1\n")
        self.b.write_bytes(b"other = 2\n")
        self.config = Config(
            self.root,
            self.a,
            state_directory=self.base / "state",
            writable_roots=(self.root,),
            mutations_enabled=True,
            request_timeout_seconds=5,
        )
        self.session = FakeSession()
        self.rpc = RenameRpc()
        self.session.rpc = self.rpc
        self.session.capabilities["renameProvider"] = {"prepareProvider": True}
        self.documents = Documents(Workspace(self.config), cast("Session", self.session))
        await self.documents.start()
        self.transactions = MemoryTransactions()
        self.transactions.paths = {p.as_uri(): p for p in (self.a, self.b)}
        self.mutations: Any = Mutations(
            self.config,
            self.documents,
            cast("Session", self.session),
            cast("Transactions", self.transactions),
        )
        await self.mutations.start()
        self.addAsyncCleanup(self.documents.close)

    def hashes(self):
        return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (self.a, self.b)}

    def edit(self):
        return TextEdit(Range(Position(0, 8), Position(0, 9)), "9")

    async def preview(self):
        return await self.mutations.preview_edit(
            self.a.as_uri(), [self.edit()], self.hashes()["a.py"]
        )

    async def test_disabled_and_claimed_approval_denied(self):
        before = self.hashes()
        self.mutations.config = replace(self.config, mutations_enabled=False)
        with self.assertRaises(AdapterError) as denied:
            await self.preview()
        self.assertEqual(denied.exception.code, "MUTATIONS_DISABLED")
        self.assertEqual(before, self.hashes())
        self.assertNotIn("apply", self.transactions.calls)

    async def test_preview_immutable_no_write(self):
        before = self.hashes()
        preview = await self.preview()
        self.assertEqual(before, self.hashes())
        self.assertNotIn("apply", self.transactions.calls)
        self.assertIn("-value = 1", preview["result"]["files"][0]["diff"])
        preview["result"]["files"][0]["diff"] = "forged"
        applied = await self.mutations.apply(preview["result"]["plan_id"])
        self.assertEqual(applied["result"]["status"], "committed")
        self.assertEqual(self.a.read_bytes(), b"value = 9\n")
        retry = await self.mutations.apply(preview["result"]["plan_id"])
        self.assertEqual(retry["result"], applied["result"])
        self.assertEqual(self.transactions.calls.count("apply"), 1)

    async def test_stale_apply_is_not_replanned(self):
        preview = await self.preview()
        self.b.write_bytes(b"changed = True\n")
        before = self.hashes()
        with self.assertRaises(AdapterError) as stale:
            await self.mutations.apply(preview["result"]["plan_id"])
        self.assertEqual(stale.exception.code, "STALE_DOCUMENT")
        self.assertEqual(before, self.hashes())
        self.assertNotIn("apply", self.transactions.calls)
        self.assertFalse(self.rpc.requests)

    async def test_rename_prepare_and_null(self):
        self.rpc.edit = {
            "changes": {
                self.a.as_uri(): [
                    {
                        "range": self.rpc.prepare,
                        "newText": "renamed",
                    }
                ]
            }
        }
        preview = await self.mutations.preview_rename(self.a.as_uri(), Position(0, 0), "renamed")
        self.assertEqual(len(preview["result"]["files"]), 1)
        self.assertEqual(
            [m for m, _ in self.rpc.requests],
            ["textDocument/prepareRename", "textDocument/rename"],
        )
        self.rpc.prepare = None
        before = len(self.rpc.requests)
        with self.assertRaises(AdapterError):
            await self.mutations.preview_rename(self.a.as_uri(), Position(0, 0), "renamed")
        self.assertEqual(len(self.rpc.requests), before + 1)
        for name in ("class", "bad-name", "", "1value"):
            with self.assertRaises(AdapterError) as invalid:
                await self.mutations.preview_rename(self.a.as_uri(), Position(0, 0), name)
            self.assertEqual(invalid.exception.code, "INVALID_INPUT")
        self.assertEqual(self.a.read_bytes(), b"value = 1\n")

    async def test_annotations_remain_destructive(self):
        self.rpc.edit = {
            "documentChanges": [
                {
                    "textDocument": {"uri": self.a.as_uri(), "version": 1},
                    "edits": [
                        {
                            "range": self.rpc.prepare,
                            "newText": "renamed",
                            "annotationId": "review",
                        }
                    ],
                }
            ],
            "changeAnnotations": {"review": {"label": "Review rename", "needsConfirmation": True}},
        }
        preview = await self.mutations.preview_rename(self.a.as_uri(), Position(0, 0), "renamed")
        self.assertTrue(preview["result"]["annotations"][0]["needs_confirmation"])
        self.assertNotIn("apply", self.transactions.calls)

    async def test_apply_drains_readers_before_preflight(self):
        preview = await self.preview()
        async with self.documents.generation():
            apply = asyncio.create_task(self.mutations.apply(preview["result"]["plan_id"]))
            await until(lambda: self.documents._exclusive)
            self.assertFalse(self.transactions.started.is_set())
            self.assertEqual(self.a.read_bytes(), b"value = 1\n")
        self.assertEqual((await apply)["result"]["status"], "committed")

    async def test_read_admission_blocked_during_commit_and_no_restart(self):
        preview = await self.preview()
        self.transactions.release.clear()
        apply = asyncio.create_task(self.mutations.apply(preview["result"]["plan_id"]))
        self.addCleanup(self.transactions.release.set)
        await until(self.transactions.started.is_set)
        with self.assertRaises(AdapterError) as busy:
            async with self.documents.generation():
                self.fail("Read admitted during commit")
        self.assertEqual(busy.exception.code, "WORKSPACE_BUSY")
        self.assertEqual(self.session.events, [])
        self.transactions.release.set()
        self.assertEqual((await apply)["result"]["status"], "committed")
        async with self.documents.generation() as fresh:
            self.assertNotEqual(fresh.generation, preview["workspace_generation"])

    async def test_apply_drain_timeout_writes_nothing(self):
        preview = await self.preview()
        before = self.hashes()
        async with self.documents.generation():
            self.documents.workspace.config = replace(self.config, request_timeout_seconds=0.05)
            try:
                with self.assertRaises(AdapterError) as timeout:
                    await self.mutations.apply(preview["result"]["plan_id"])
                self.assertEqual(timeout.exception.code, "WORKSPACE_BUSY")
            finally:
                self.documents.workspace.config = self.config
        self.assertFalse(self.transactions.started.is_set())
        self.assertEqual(before, self.hashes())
        async with self.documents.generation():
            pass

    async def test_cancel_while_draining_releases_admission_without_writes(self):
        preview = await self.preview()
        async with self.documents.generation():
            apply = asyncio.create_task(self.mutations.apply(preview["result"]["plan_id"]))
            await until(lambda: self.documents._exclusive)
            apply.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await apply
            self.assertFalse(self.transactions.started.is_set())
            self.assertFalse(self.documents._exclusive)
        async with self.documents.generation():
            pass

    async def test_cancel_during_apply_does_not_lose_receipt(self):
        preview = await self.preview()
        self.transactions.release.clear()
        self.addCleanup(self.transactions.release.set)
        apply = asyncio.create_task(self.mutations.apply(preview["result"]["plan_id"]))
        await until(self.transactions.started.is_set)
        apply.cancel()
        await asyncio.sleep(0)
        self.assertFalse(apply.done())
        self.transactions.release.set()
        with self.assertRaises(asyncio.CancelledError):
            await apply
        receipt = self.transactions.receipt(preview["result"]["plan_id"])
        self.assertEqual(receipt["status"], "committed")
        retry = await self.mutations.apply(preview["result"]["plan_id"])
        self.assertEqual(retry["result"], receipt)

    async def test_committed_but_sync_failed_is_not_rollback(self):
        preview = await self.preview()
        original = self.documents.committed

        async def fail(snapshots):
            await original(())
            raise AdapterError("SERVER_EXITED", "Synthetic synchronization failure")

        with patch.object(self.documents, "committed", side_effect=fail):
            applied = await self.mutations.apply(preview["result"]["plan_id"])
        self.assertEqual(applied["result"]["status"], "committed")
        self.assertEqual(applied["semantic_state"], "unavailable")
        self.assertTrue(self.documents.invalidated.is_set())
        self.assertEqual(self.a.read_bytes(), b"value = 9\n")

    async def test_preview_bounds_expiry_and_complete_rejection(self):
        self.mutations.config = replace(
            self.config, limits=replace(self.config.limits, retained_plans=1)
        )
        first = await self.preview()
        with self.assertRaises(AdapterError) as full:
            await self.preview()
        self.assertEqual(full.exception.code, "LIMIT_EXCEEDED")
        self.mutations.plans[first["result"]["plan_id"]] = replace(
            self.mutations.plans[first["result"]["plan_id"]], expires_at=0
        )
        with self.assertRaises(AdapterError) as expired:
            await self.mutations.apply(first["result"]["plan_id"])
        self.assertEqual(expired.exception.code, "PLAN_EXPIRED")
        before = self.hashes()
        for edits, expected in (
            ([self.edit(), self.edit()], before["a.py"]),
            ([self.edit()], "0" * 64),
        ):
            with self.assertRaises(AdapterError):
                await self.mutations.preview_edit(self.a.as_uri(), edits, expected)
        self.assertEqual(before, self.hashes())

    async def test_cancelled_recovery_failure_does_not_open_admission(self):
        self.mutations.ready = False
        started = threading.Event()
        release = threading.Event()
        self.addCleanup(release.set)

        def recover():
            started.set()
            if not release.wait(10):
                raise AssertionError("Recovery release timeout")
            raise OSError("Synthetic recovery IO failure")

        with patch.object(self.transactions, "recover", side_effect=recover):
            task = asyncio.create_task(self.mutations.start())
            await until(started.is_set)
            task.cancel()
            await asyncio.sleep(0)
            release.set()
            with self.assertRaises(asyncio.CancelledError):
                await task
        self.assertFalse(self.mutations.ready)

    async def test_preview_reserves_complete_receipt_result_budget(self):
        from gz_mcp_lsp.results import encoded_size

        preview = await self.mutations.preview_edit(self.a.as_uri(), [], self.hashes()["a.py"])
        self.mutations.config = replace(
            self.config, limits=replace(self.config.limits, result_bytes=encoded_size(preview) + 10)
        )
        before = self.hashes()
        with self.assertRaises(AdapterError) as limited:
            await self.mutations.preview_edit(self.a.as_uri(), [], before["a.py"])
        self.assertEqual(limited.exception.code, "RESULT_LIMIT")
        self.assertEqual(before, self.hashes())
        self.assertNotIn("apply", self.transactions.calls)

    async def test_untrusted_rename_rejects_entire_target_set(self):
        outside = self.base / "outside.py"
        outside.write_bytes(b"private = 1\n")
        valid = {"range": self.rpc.prepare, "newText": "renamed"}
        edits = [
            {"changes": {self.a.as_uri(): [valid], outside.as_uri(): [valid]}},
            {"documentChanges": [{"kind": "delete", "uri": self.a.as_uri()}]},
            {
                "documentChanges": [
                    {"textDocument": {"uri": self.a.as_uri(), "version": 99}, "edits": [valid]}
                ]
            },
            {"changes": {self.a.as_uri(): [valid | {"annotationId": "missing"}]}},
            {"changes": {self.a.as_uri(): [valid]}, "documentChanges": []},
        ]
        before = self.hashes()
        for edit in edits:
            with self.subTest(edit=edit):
                self.rpc.edit = edit
                with self.assertRaises(AdapterError):
                    await self.mutations.preview_rename(self.a.as_uri(), Position(0, 0), "renamed")
                self.assertEqual(before, self.hashes())
                self.assertEqual(outside.read_bytes(), b"private = 1\n")
        self.assertNotIn("apply", self.transactions.calls)

    async def test_mutation_successes_follow_common_result_envelope(self):
        preview = await self.preview()
        applied = await self.mutations.apply(preview["result"]["plan_id"])
        for response in (preview, applied):
            with self.subTest(action=response.get("action")):
                self.assertTrue(
                    {
                        "schema_version",
                        "operation",
                        "position_encoding",
                        "result",
                        "workspace_generation",
                        "documents",
                        "complete",
                    }
                    <= response.keys()
                )
                self.assertEqual(response["position_encoding"], "utf-16")
                self.assertTrue(response["complete"])
