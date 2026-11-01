"""Guarded transaction failures, durable receipts and zero-write denials."""

import hashlib
import os
import stat
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.edit_plan import plan_workspace_edit
from gz_mcp_lsp.models import AdapterError, Json
from gz_mcp_lsp.workspace import Workspace


class TransactionFixture(unittest.TestCase):
    """Use a private directory on the native home filesystem, never a network mount."""

    def setUp(self):
        try:
            from gz_mcp_lsp.filesystem import Transactions
        except ImportError as error:
            self.fail(f"Guarded filesystem transactions absent: {error}")
        self.transaction_type = Transactions
        self.temporary = tempfile.TemporaryDirectory(prefix="gz-transactions-", dir=Path.home())
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.root = self.base / "workspace"
        self.root.mkdir(mode=0o700)
        self.state = self.base / "state"
        self.a = self.root / "a.py"
        self.b = self.root / "b.py"
        self.a.write_bytes(b"first = 1\r\n")
        self.b.write_bytes(b"second = 2\n")
        self.a.chmod(0o640)
        self.b.chmod(0o600)
        self.config = Config(
            self.root,
            Path(sys.executable),
            state_directory=self.state,
            writable_roots=(self.root,),
            mutations_enabled=True,
        )
        self.workspace = Workspace(self.config)

    def plan(self):
        """Preview exact preimages without filesystem writes."""
        snapshots = {path.as_uri(): self.workspace.read(path.as_uri()) for path in (self.a, self.b)}
        edits: dict[str, Json] = {
            uri: [
                {
                    "range": {
                        "start": {"line": 0, "character": 0},
                        "end": {"line": 1, "character": 0},
                    },
                    "newText": "first = 10\r\n" if uri == self.a.as_uri() else "second = 20\n",
                }
            ]
            for uri in snapshots
        }
        return plan_workspace_edit({"changes": edits}, snapshots, "synthetic-generation")

    def images(self):
        return {
            path.name: (
                hashlib.sha256(path.read_bytes()).hexdigest(),
                stat.S_IMODE(path.stat().st_mode),
            )
            for path in (self.a, self.b)
        }

    def transactions(self, config=None):
        return self.transaction_type(config or self.config, self.workspace)


class DenialTests(TransactionFixture):
    """These denials run on Windows as well as supported POSIX hosts."""

    def test_disabled_and_unsupported_change_no_files(self):
        before = self.images()
        plan = self.plan()
        with self.assertRaises(AdapterError) as disabled:
            self.transactions(replace(self.config, mutations_enabled=False)).apply(plan)
        self.assertEqual(disabled.exception.code, "MUTATIONS_DISABLED")
        self.assertFalse(self.state.exists())
        if os.name == "nt":
            for operation in ("apply", "recover"):
                with self.assertRaises(AdapterError) as unsupported:
                    adapter = self.transactions()
                    adapter.apply(plan) if operation == "apply" else adapter.recover()
                self.assertEqual(unsupported.exception.code, "UNSUPPORTED")
            self.assertFalse(self.state.exists())
        self.assertEqual(before, self.images())


@unittest.skipIf(
    os.name == "nt", "POSIX-only mutation adapter; Windows denial is tested separately"
)
class FilesystemTests(TransactionFixture):
    """Fault injection patches source replacement, never skips required POSIX capabilities."""

    def test_denied_target_changes_zero_files(self):
        before = self.images()
        allowed = self.root / "allowed"
        allowed.mkdir()
        with self.assertRaises(AdapterError) as denied:
            self.transactions(replace(self.config, writable_roots=(allowed,))).apply(self.plan())
        self.assertEqual(denied.exception.code, "OUTSIDE_WORKSPACE")
        self.assertEqual(before, self.images())
        with self.assertRaises(AdapterError):
            self.transactions(replace(self.config, state_directory=self.root / "state")).apply(
                self.plan()
            )
        self.assertEqual(before, self.images())

    def test_preflight_all_targets_before_replace(self):
        plan = self.plan()
        self.b.write_bytes(b"new external content\n")
        before = self.images()
        adapter = self.transactions()
        with (
            patch.object(adapter, "_replace", wraps=adapter._replace) as replacement,
            self.assertRaises(AdapterError) as conflict,
        ):
            adapter.apply(plan)
        self.assertEqual(conflict.exception.code, "CONFLICT")
        replacement.assert_not_called()
        self.assertEqual(before, self.images())

    def test_parent_symlink_swap_and_hardlink(self):
        plan = self.plan()
        alias = self.base / "hardlink"
        os.link(self.a, alias)
        before = self.images()
        with self.assertRaises(AdapterError):
            self.transactions().apply(plan)
        self.assertEqual(before, self.images())
        alias.unlink()
        plan = self.plan()
        outside = self.base / "outside"
        outside.mkdir()
        for name in ("a.py", "b.py"):
            (outside / name).write_bytes(b"DO NOT TOUCH\n")
        adapter = self.transactions()
        original = adapter._write_journal
        moved = self.base / "moved"
        swapped = False

        def swap(descriptor, record):
            nonlocal swapped
            original(descriptor, record)
            if record["phase"] == "prepared" and not swapped:
                swapped = True
                self.root.rename(moved)
                self.root.symlink_to(outside, target_is_directory=True)

        with patch.object(adapter, "_write_journal", side_effect=swap):
            receipt = adapter.apply(plan)
        self.assertEqual(receipt["status"], "recovery_required")
        self.assertEqual((outside / "a.py").read_bytes(), b"DO NOT TOUCH\n")
        self.assertEqual((outside / "b.py").read_bytes(), b"DO NOT TOUCH\n")
        self.assertEqual((moved / "a.py").read_bytes(), b"first = 1\r\n")
        self.assertEqual((moved / "b.py").read_bytes(), b"second = 2\n")

    def test_failure_at_each_replace_rolls_back(self):
        for fail_at in (1, 2):
            for after_replace in (False, True):
                with self.subTest(fail_at=fail_at, after=after_replace):
                    plan = self.plan()
                    before_bytes = self.images()
                    adapter = self.transactions()
                    original = adapter._replace
                    count = 0

                    def fail(
                        *args, fail_at=fail_at, after_replace=after_replace, original=original
                    ):
                        nonlocal count
                        count += 1
                        if count == fail_at and not after_replace:
                            raise OSError("Synthetic replacement failure")
                        original(*args)
                        if count == fail_at and after_replace:
                            raise OSError("Synthetic failure after replacement")

                    with patch.object(adapter, "_replace", side_effect=fail):
                        receipt = adapter.apply(plan)
                    after_failure_bytes = self.images()
                    self.assertEqual(after_failure_bytes, before_bytes)
                    self.assertEqual(receipt["status"], "rolled_back")
                    self.assertTrue(
                        all(
                            item["status"] in {"not_written", "restored"}
                            for item in receipt["files"]
                        )
                    )

    def test_external_change_during_rollback_requires_recovery(self):
        adapter = self.transactions()
        original = adapter._replace
        count = 0

        def conflict(*args):
            nonlocal count
            count += 1
            if count == 2:
                self.a.write_bytes(b"newer external writer\n")
                raise OSError("Synthetic second replacement failure")
            original(*args)

        with patch.object(adapter, "_replace", side_effect=conflict):
            receipt = adapter.apply(self.plan())
        self.assertEqual(receipt["status"], "recovery_required")
        self.assertEqual(self.a.read_bytes(), b"newer external writer\n")
        self.assertEqual(self.b.read_bytes(), b"second = 2\n")
        before = self.images()
        with self.assertRaises(AdapterError) as blocked:
            self.transactions().apply(self.plan())
        self.assertEqual(blocked.exception.code, "RECOVERY_REQUIRED")
        self.assertEqual(before, self.images())

    def test_lost_response_replay_once(self):
        plan = self.plan()
        adapter = self.transactions()
        with patch.object(adapter, "_replace", wraps=adapter._replace) as replacement:
            committed = adapter.apply(plan)
            replace_count_before_retry = replacement.call_count
            retry = adapter.apply(replace(plan, expires_at=0))
            replace_count_after_retry = replacement.call_count
        self.assertEqual(committed["status"], "committed")
        self.assertEqual(retry, committed)
        self.assertEqual(replace_count_after_retry, replace_count_before_retry)
        self.assertEqual(replace_count_before_retry, 2)
        restarted = self.transactions()
        self.assertEqual(restarted.receipt(plan.plan_id), committed)
        self.assertEqual(restarted.apply(replace(plan, expires_at=0)), committed)
        self.assertEqual(self.a.read_bytes(), b"first = 10\r\n")
        self.assertEqual(stat.S_IMODE(self.a.stat().st_mode), 0o640)
        self.assertEqual(stat.S_IMODE(self.b.stat().st_mode), 0o600)

    def test_change_after_journal_before_replace_is_preserved(self):
        adapter = self.transactions()
        original = adapter._write_journal
        changed = False

        def change(descriptor, record):
            nonlocal changed
            original(descriptor, record)
            if record["files"][0]["status"] == "replace_intent" and not changed:
                changed = True
                self.a.write_bytes(b"external after intent\n")

        with patch.object(adapter, "_write_journal", side_effect=change):
            receipt = adapter.apply(self.plan())
        self.assertEqual(receipt["status"], "recovery_required")
        self.assertEqual(self.a.read_bytes(), b"external after intent\n")
        self.assertEqual(self.b.read_bytes(), b"second = 2\n")

    def test_lock_and_private_state_deny_without_source_changes(self):
        adapter = self.transactions()
        before = self.images()
        with adapter._state(), self.assertRaises(AdapterError) as busy:
            self.transactions().apply(self.plan())
        self.assertEqual(busy.exception.code, "WORKSPACE_BUSY")
        self.state.chmod(0o755)
        with self.assertRaises(AdapterError) as unsafe:
            self.transactions().apply(self.plan())
        self.assertEqual(unsafe.exception.code, "RECOVERY_REQUIRED")
        self.assertEqual(self.images(), before)

    def test_malformed_receipt_fails_closed(self):
        import json

        plan = self.plan()
        self.transactions().apply(plan)
        receipt_path = self.state / plan.plan_id / "receipt.json"
        original = json.loads(receipt_path.read_text(encoding="utf-8"))["record"]
        for update in ({"status": []}, {"files": [None]}, {"files": [{"uri": 17}]}):
            with self.subTest(update=update):
                record = original | update
                body = json.dumps(
                    record, sort_keys=True, separators=(",", ":"), ensure_ascii=False
                ).encode()
                receipt_path.write_text(
                    json.dumps({"record": record, "sha256": hashlib.sha256(body).hexdigest()}),
                    encoding="utf-8",
                )
                before = self.images()
                with self.assertRaises(AdapterError) as error:
                    self.transactions().receipt(plan.plan_id)
                self.assertEqual(error.exception.code, "RECOVERY_REQUIRED")
                self.assertEqual(self.images(), before)

    def test_no_op_preserves_target_identity(self):
        from gz_mcp_lsp.edit_plan import PlannedFile, plan_digest

        plan = self.plan()
        files = tuple(PlannedFile(f.uri, f.before, f.before.data, ()) for f in plan.files)
        plan = replace(plan, files=files)
        plan = replace(plan, plan_id=plan_digest(plan))
        before = [path.stat().st_ino for path in (self.a, self.b)]
        adapter = self.transactions()
        with patch.object(adapter, "_replace", side_effect=AssertionError("No-op replaced source")):
            receipt = adapter.apply(plan)
        self.assertEqual(receipt["status"], "no_op")
        self.assertEqual(before, [path.stat().st_ino for path in (self.a, self.b)])

    def test_state_quota_and_corrupt_journal(self):
        before = self.images()
        limits = replace(self.config.limits, retained_state_bytes=64)
        with self.assertRaises(AdapterError) as quota:
            self.transactions(replace(self.config, limits=limits)).apply(self.plan())
        self.assertEqual(quota.exception.code, "LIMIT_EXCEEDED")
        self.assertEqual(before, self.images())
        plan = self.plan()
        self.transactions().apply(plan)
        before = self.images()
        journal = self.state / plan.plan_id / "journal.json"
        journal.write_bytes(b"{")
        recovery = self.transactions().recover()
        self.assertTrue(any(receipt["status"] == "recovery_required" for receipt in recovery))
        self.assertEqual(before, self.images())
        with self.assertRaises(AdapterError) as blocked:
            self.transactions().apply(self.plan())
        self.assertEqual(blocked.exception.code, "RECOVERY_REQUIRED")
