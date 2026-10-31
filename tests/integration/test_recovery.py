"""Actual process exits test durability; mocked exceptions cannot prove crash recovery."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.filesystem import Transactions
from gz_mcp_lsp.models import AdapterError
from gz_mcp_lsp.workspace import Workspace
from tests.test_filesystem import FilesystemFixture


class RecoveryTests(FilesystemFixture):
    """Every checkpoint runs in a fresh state/source directory."""

    def test_crash_at_journal_stage_replace_and_receipt_boundaries(self):
        checkpoints = [
            "registered",
            "journal",
            "before:0",
            "staged:0",
            "before:1",
            "staged:1",
            "prepared",
            "replace:0",
            "replace:1",
            "rollback:0",
            "rollback:1",
            "receipt",
        ]
        for checkpoint in checkpoints:
            with self.subTest(checkpoint=checkpoint), tempfile.TemporaryDirectory() as name:
                base = Path(name).resolve()
                root, state = base / "workspace", base / "state"
                root.mkdir()
                a, b = root / "a.py", root / "b.py"
                a.write_bytes(b"a = 1\r\n")
                b.write_bytes(b"b = 2\n")
                a.chmod(0o640)
                b.chmod(0o600)
                before = [(p.read_bytes(), p.stat().st_mode) for p in (a, b)]
                crashed = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "tests.support.transaction_driver",
                        str(root),
                        str(state),
                        checkpoint,
                    ],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=15,
                    check=False,
                )
                self.assertEqual(crashed.returncode, 77, crashed.stderr)
                config = Config(
                    root,
                    Path("/usr/bin/true"),
                    state_directory=state,
                    writable_roots=(root,),
                    mutations_enabled=True,
                )
                if checkpoint == "registered":
                    # Index durability precedes journal creation: missing metadata must fail closed.
                    with self.assertRaises(AdapterError) as failure:
                        Transactions(config, Workspace(config))
                    self.assertEqual(failure.exception.code, "RECOVERY_REQUIRED")
                    self.assertEqual([(p.read_bytes(), p.stat().st_mode) for p in (a, b)], before)
                    continue
                transaction = Transactions(config, Workspace(config))
                try:
                    receipts = transaction.recover()
                    self.assertFalse(transaction.blocked, receipts)
                    self.assertEqual(len(receipts), 1)
                    expected_status = "committed" if checkpoint == "receipt" else "rolled_back"
                    self.assertEqual(receipts[0]["status"], expected_status)
                    if expected_status == "rolled_back":
                        self.assertEqual(
                            [(p.read_bytes(), p.stat().st_mode) for p in (a, b)], before
                        )
                    else:
                        self.assertEqual(
                            (a.read_bytes(), b.read_bytes()), (b"z = 1\r\n", b"z = 2\n")
                        )
                    self.assertFalse(list(root.glob(".gz-mcp-lsp-*")))
                finally:
                    transaction.close()

    def test_missing_recovery_copy_blocks_instead_of_fabricating_rollback(self):
        crashed = subprocess.run(
            [
                sys.executable,
                "-m",
                "tests.support.transaction_driver",
                str(self.root),
                str(self.state),
                "replace:0",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
            check=False,
        )
        self.assertEqual(crashed.returncode, 77, crashed.stderr)
        backup = next(self.root.glob("*-0.before"))
        backup.unlink()
        before_restart = self.images()
        transaction = self.transaction()
        self.assertTrue(transaction.blocked)
        receipts = transaction.recover()
        self.assertEqual(receipts[0]["status"], "recovery_required")
        self.assertEqual(self.images(), before_restart)
        state = json.loads((self.state / ".index.json").read_text())
        self.assertEqual(len(state["ids"]), 1)
