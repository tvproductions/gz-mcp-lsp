"""Disposable filesystem transactions with injected failures and identity conflicts."""

import json
import os
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from gz_mcp_lsp.config import Config, Limits
from gz_mcp_lsp.edit_plan import plan_workspace_edit
from gz_mcp_lsp.filesystem import Transactions
from gz_mcp_lsp.models import AdapterError
from gz_mcp_lsp.workspace import Workspace


def edit_set(uri, replacement):
    return {
        uri: [
            {
                "range": {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 1}},
                "newText": replacement,
            }
        ]
    }


class FilesystemFixture(unittest.TestCase):
    """Every mutation is confined to a newly created synthetic temporary directory."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.root = self.base / "workspace"
        self.root.mkdir()
        self.state = self.base / "state"
        self.a, self.b = self.root / "a.py", self.root / "b.py"
        self.a.write_bytes(b"a = 1\r\n")
        self.b.write_bytes(b"b = 2\n")
        self.a.chmod(0o640)
        self.b.chmod(0o600)
        self.config = Config(
            self.root,
            Path("/usr/bin/true"),
            state_directory=self.state,
            writable_roots=(self.root,),
            mutations_enabled=True,
        )
        self.workspace = Workspace(self.config)

    def transaction(self):
        transaction = Transactions(self.config, self.workspace)
        self.addCleanup(transaction.close)
        return transaction

    def plan(self, paths=None):
        targets = paths or [self.a, self.b]
        snapshots = {path.as_uri(): self.workspace.read(path.as_uri()) for path in targets}
        changes = {}
        for index, path in enumerate(targets):
            changes.update(edit_set(path.as_uri(), "x" if index == 0 else "y"))
        return plan_workspace_edit({"changes": changes}, snapshots, self.workspace.manifest())

    def images(self):
        return [(p.read_bytes(), p.stat().st_mode) for p in (self.a, self.b)]


class FilesystemTests(FilesystemFixture):
    """Truthful complete outcomes matter more than a non-error tool response."""

    def test_corrupt_index_values_fail_closed_with_recovery_error(self):
        transaction = self.transaction()
        transaction.close()
        before = self.images()
        (self.state / ".index.json").write_text(
            json.dumps({"schema_version": 1, "ids": [{}]}), encoding="utf-8"
        )
        with self.assertRaises(AdapterError) as failure:
            self.transaction()
        self.assertEqual(failure.exception.code, "RECOVERY_REQUIRED")
        self.assertEqual(self.images(), before)

    def test_corrupt_journal_status_fails_closed_with_recovery_error(self):
        transaction = self.transaction()
        plan = self.plan()
        transaction.apply(plan)
        transaction.close()
        path = self.state / f"{plan.plan_id}.json"
        journal = json.loads(path.read_text(encoding="utf-8"))
        journal["status"] = {}
        path.write_text(json.dumps(journal), encoding="utf-8")
        before = self.images()
        with self.assertRaises(AdapterError) as failure:
            self.transaction()
        self.assertEqual(failure.exception.code, "RECOVERY_REQUIRED")
        self.assertEqual(self.images(), before)

    def test_disabled_and_denied_target_change_zero_files(self):
        before = self.images()
        with self.assertRaises(AdapterError):
            Transactions(replace(self.config, mutations_enabled=False), self.workspace)
        plan = self.plan()
        transaction = self.transaction()
        transaction.config = replace(self.config, writable_roots=(self.root / "other",))
        with self.assertRaises(AdapterError):
            transaction.apply(plan)
        self.assertEqual(self.images(), before)

    def test_nested_nonlocal_volume_is_denied_before_source_writes(self):
        transaction = self.transaction()
        plan = self.plan()
        before = self.images()
        with (
            patch("gz_mcp_lsp.filesystem.local_volume", return_value=False),
            self.assertRaises(AdapterError) as failure,
        ):
            transaction.apply(plan)
        self.assertEqual(failure.exception.code, "UNSUPPORTED")
        self.assertEqual(self.images(), before)

    def test_preflight_all_targets_before_replace(self):
        plan = self.plan()
        self.b.write_bytes(b"external newer bytes\n")
        before = self.images()
        with self.assertRaises(AdapterError) as failure:
            self.transaction().apply(plan)
        self.assertEqual(failure.exception.code, "CONFLICT")
        self.assertEqual(self.images(), before)

    def test_failure_at_each_replace_restores_exact_bytes_and_modes(self):
        transaction = self.transaction()
        before = self.images()
        for target in ["prepared", "replace:0", "replace:1"]:

            def checkpoint(event, expected=target):
                if event == expected:
                    raise OSError("injected ordinary IO failure")

            with patch.object(transaction, "_checkpoint", side_effect=checkpoint):
                receipt = transaction.apply(self.plan())
            self.assertEqual(receipt["status"], "rolled_back")
            self.assertEqual(self.images(), before)

    def test_external_write_during_rollback_preserved_and_requires_recovery(self):
        transaction = self.transaction()
        plan = self.plan()

        def checkpoint(event):
            if event == "replace:0":
                self.a.write_bytes(b"external content\n")
                raise OSError("injected after external writer")

        with patch.object(transaction, "_checkpoint", side_effect=checkpoint):
            receipt = transaction.apply(plan)
        self.assertEqual(receipt["status"], "recovery_required")
        self.assertEqual(self.a.read_bytes(), b"external content\n")
        self.assertEqual(self.b.read_bytes(), b"b = 2\n")
        with self.assertRaises(AdapterError) as failure:
            transaction.apply(self.plan())
        self.assertEqual(failure.exception.code, "RECOVERY_REQUIRED")

    def test_lost_response_replay_returns_durable_receipt_without_replacement(self):
        transaction = self.transaction()
        plan = self.plan()
        receipt = transaction.apply(plan)
        self.assertEqual(receipt["status"], "committed")
        self.assertEqual(self.a.read_bytes(), b"x = 1\r\n")
        self.assertEqual(self.b.read_bytes(), b"y = 2\n")
        with patch("os.replace", side_effect=AssertionError("replayed transaction wrote again")):
            self.assertEqual(transaction.apply(plan), receipt)
        transaction.close()
        reopened = self.transaction()
        with patch("os.replace", side_effect=AssertionError("receipt lookup wrote")):
            self.assertEqual(reopened.receipt(plan.plan_id), receipt)

    def test_parent_swap_hardlink_and_mode_change_are_denied(self):
        plan = self.plan()
        os.link(self.a, self.root / "alias")
        with self.assertRaises(AdapterError):
            self.transaction().apply(plan)
        self.assertEqual(self.a.read_bytes(), b"a = 1\r\n")
        (self.root / "alias").unlink()

    def test_target_symlink_and_mode_changes_after_preview_are_denied(self):
        plan = self.plan()
        self.a.chmod(0o600)
        before = self.images()
        with self.assertRaises(AdapterError) as failure:
            self.transaction().apply(plan)
        self.assertEqual(failure.exception.code, "CONFLICT")
        self.assertEqual(self.images(), before)

        self.a.chmod(0o640)
        plan = self.plan()
        self.a.rename(self.root / "original.py")
        outside = self.base / "outside.py"
        outside.write_bytes(b"external bytes\n")
        self.a.symlink_to(outside)
        with self.assertRaises(AdapterError):
            self.transaction().apply(plan)
        self.assertEqual(outside.read_bytes(), b"external bytes\n")
        self.assertEqual((self.root / "original.py").read_bytes(), b"a = 1\r\n")
        self.assertEqual(self.b.read_bytes(), b"b = 2\n")

    def test_restore_io_failure_is_truthful_and_blocks_next_transaction(self):
        transaction = self.transaction()
        plan = self.plan()
        real_replace = os.replace

        def checkpoint(event):
            if event == "replace:0":
                raise OSError("start rollback")

        def fail_restore(source, destination, **kwargs):
            if str(source).endswith(".restore"):
                raise OSError("restore unavailable")
            return real_replace(source, destination, **kwargs)

        with (
            patch.object(transaction, "_checkpoint", side_effect=checkpoint),
            patch("os.replace", side_effect=fail_restore),
        ):
            receipt = transaction.apply(plan)
        self.assertEqual(receipt["status"], "recovery_required")
        self.assertEqual(
            receipt["files"],
            [
                {"uri": self.a.as_uri(), "status": "unknown"},
                {"uri": self.b.as_uri(), "status": "before"},
            ],
        )
        self.assertEqual(self.a.read_bytes(), b"x = 1\r\n")
        self.assertEqual(self.b.read_bytes(), b"b = 2\n")
        transaction.close()
        reopened = self.transaction()
        self.assertTrue(reopened.blocked)
        self.assertEqual(reopened.receipt(plan.plan_id), receipt)
        with self.assertRaises(AdapterError) as failure:
            reopened.apply(self.plan())
        self.assertEqual(failure.exception.code, "RECOVERY_REQUIRED")

    def test_parent_identity_change_without_file_content_change_is_denied(self):
        package = self.root / "package"
        package.mkdir()
        path = package / "module.py"
        path.write_text("a = 1\n")
        plan = self.plan([path])
        original = self.root / "original"
        package.rename(original)
        package.mkdir()
        (original / "module.py").rename(path)
        with self.assertRaises(AdapterError):
            self.transaction().apply(plan)
        self.assertEqual(path.read_text(), "a = 1\n")

    def test_parent_symlink_swap_cannot_modify_external_file(self):
        package = self.root / "package"
        package.mkdir()
        path = package / "module.py"
        path.write_text("a = 1\n")
        plan = self.plan([path])
        package.rename(self.root / "original")
        outside = self.base / "external"
        outside.mkdir()
        external = outside / "module.py"
        external.write_text("external\n")
        package.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(AdapterError):
            self.transaction().apply(plan)
        self.assertEqual(external.read_text(), "external\n")

    def test_corrupt_or_missing_registered_journal_fails_closed(self):
        transaction = self.transaction()
        plan = self.plan()
        transaction.apply(plan)
        transaction.close()
        (self.state / f"{plan.plan_id}.json").write_text("corrupt")
        before = self.images()
        with self.assertRaises(AdapterError) as failure:
            self.transaction()
        self.assertEqual(failure.exception.code, "RECOVERY_REQUIRED")
        self.assertEqual(self.images(), before)

    def test_state_quota_exhaustion_rejects_before_source_writes(self):
        self.config = replace(self.config, limits=replace(Limits(), max_state_bytes=200))
        before = self.images()
        with self.assertRaises(AdapterError) as failure:
            self.transaction().apply(self.plan())
        self.assertEqual(failure.exception.code, "LIMIT_EXCEEDED")
        self.assertEqual(self.images(), before)

    def test_single_writer_lock_and_private_state(self):
        self.transaction()
        with self.assertRaises(AdapterError) as failure:
            self.transaction()
        self.assertEqual(failure.exception.code, "WORKSPACE_BUSY")
        self.assertEqual(self.state.stat().st_mode & 0o777, 0o700)

    def test_no_op_preserves_source_inode_and_creates_no_source_stages(self):
        snapshots = {self.a.as_uri(): self.workspace.read(self.a.as_uri())}
        plan = plan_workspace_edit(
            {"changes": {self.a.as_uri(): []}}, snapshots, self.workspace.manifest()
        )
        inode = self.a.stat().st_ino
        receipt = self.transaction().apply(plan)
        self.assertEqual(receipt["status"], "no_op")
        self.assertEqual(self.a.stat().st_ino, inode)
        self.assertFalse(list(self.root.glob(".gz-mcp-lsp-*")))

    def test_durable_receipt_remains_available_after_external_source_deletion(self):
        transaction = self.transaction()
        plan = self.plan()
        receipt = transaction.apply(plan)
        self.assertEqual(receipt["status"], "committed")
        self.a.unlink()
        self.assertEqual(transaction.receipt(plan.plan_id), receipt)
