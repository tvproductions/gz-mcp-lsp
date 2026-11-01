"""Actual process death/restart at durable journal, source and receipt boundaries."""

import os
import stat
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from gz_mcp_lsp.filesystem import Transactions
from gz_mcp_lsp.models import AdapterError
from gz_mcp_lsp.workspace import Workspace
from tests.support.crash_transaction import configuration, preview


@unittest.skipIf(
    os.name == "nt", "POSIX crash safety; Windows zero-write denial runs in test_filesystem"
)
class RecoveryTests(unittest.TestCase):
    def crash(self, point):
        temporary = tempfile.TemporaryDirectory(prefix="gz-crash-", dir=Path.home())
        self.addCleanup(temporary.cleanup)
        base = Path(temporary.name).resolve()
        root = base / "workspace"
        root.mkdir(mode=0o700)
        for name, data, mode in (
            ("a.py", b"first = 1\r\n", 0o640),
            ("b.py", b"second = 2\n", 0o600),
        ):
            path = root / name
            path.write_bytes(data)
            path.chmod(mode)
        process = subprocess.run(
            [sys.executable, "-m", "tests.support.crash_transaction", str(base), point],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(process.returncode, 73, process.stdout + process.stderr)
        config = configuration(base)
        adapter = Transactions(config, Workspace(config))
        plan_id = (base / "plan-id").read_text(encoding="ascii")
        return config, adapter, plan_id

    def assert_images(self, config, committed=False):
        expected = [
            ("a.py", b"first = 10\r\n" if committed else b"first = 1\r\n", 0o640),
            ("b.py", b"second = 20\n" if committed else b"second = 2\n", 0o600),
        ]
        for name, data, mode in expected:
            path = config.workspace_root / name
            self.assertEqual(path.read_bytes(), data)
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), mode)

    def test_crash_at_each_transition_rolls_back_exactly(self):
        points = (
            "prepared",
            "replace_intent:0",
            "replace:0",
            "replaced:0",
            "replace_intent:1",
            "replace:1",
            "replaced:1",
            "rolling_back",
            "restore_intent:0",
            "restored:0",
            "rolled_back",
        )
        for point in points:
            with self.subTest(point=point):
                config, adapter, plan_id = self.crash(point)
                incomplete = preview(config, Workspace(config))
                with self.assertRaises(AdapterError) as replay:
                    adapter.apply(incomplete)
                self.assertEqual(replay.exception.code, "RECOVERY_REQUIRED")
                receipts = adapter.recover()
                self.assertEqual(len(receipts), 1)
                self.assertEqual(receipts[0]["status"], "rolled_back")
                self.assertEqual(receipts[0]["plan_id"], plan_id)
                self.assertTrue(
                    all(f["status"] in {"restored", "not_written"} for f in receipts[0]["files"])
                )
                self.assert_images(config)
                with patch.object(
                    adapter,
                    "_replace",
                    side_effect=AssertionError("Repeated recovery wrote source"),
                ):
                    self.assertEqual(adapter.recover(), receipts)
                    self.assertEqual(adapter.receipt(plan_id), receipts[0])

    def test_committed_decision_and_receipt_survive_session_and_expiry(self):
        for point in ("committed", "receipt"):
            with self.subTest(point=point):
                config, adapter, plan_id = self.crash(point)
                self.assert_images(config, committed=True)
                with patch.object(
                    adapter, "_replace", side_effect=AssertionError("Committed outcome replayed")
                ):
                    receipts = adapter.recover()
                    self.assertEqual(receipts[0]["status"], "committed")
                    self.assertEqual(adapter.receipt(plan_id), receipts[0])
                    retry = replace(
                        preview(config, Workspace(config)), plan_id=plan_id, expires_at=0
                    )
                    self.assertEqual(adapter.apply(retry), receipts[0])
                self.assert_images(config, committed=True)

    def test_external_postimage_change_is_preserved_and_locks_mutations(self):
        config, adapter, _ = self.crash("replace:0")
        a = config.workspace_root / "a.py"
        a.write_bytes(b"new external writer\n")
        receipts = adapter.recover()
        self.assertEqual(receipts[0]["status"], "recovery_required")
        self.assertEqual(receipts[0]["files"][0]["status"], "conflict")
        self.assertEqual(a.read_bytes(), b"new external writer\n")
        self.assertEqual((config.workspace_root / "b.py").read_bytes(), b"second = 2\n")
        with self.assertRaises(AdapterError) as blocked:
            adapter.apply(preview(config, Workspace(config)))
        self.assertEqual(blocked.exception.code, "RECOVERY_REQUIRED")

    def test_unpublished_journal_and_narrowed_authority_fail_closed(self):
        config, adapter, _ = self.crash("journal_before")
        receipts = adapter.recover()
        self.assertEqual(receipts[0]["status"], "recovery_required")
        self.assert_images(config)
        config, _, _ = self.crash("replace:0")
        narrowed = replace(config, writable_roots=(config.workspace_root / "allowed",))
        narrowed.writable_roots[0].mkdir()
        receipts = Transactions(narrowed, Workspace(narrowed)).recover()
        self.assertEqual(receipts[0]["status"], "recovery_required")
        self.assertEqual((config.workspace_root / "a.py").read_bytes(), b"first = 10\r\n")
        self.assertEqual((config.workspace_root / "b.py").read_bytes(), b"second = 2\n")
