"""Production installed CLI recovers crash state before accepting mutations."""

import json
import os
import subprocess
import unittest

from tests.integration.mutation_support import InstalledMutationCase


class StartupRecoveryTests(InstalledMutationCase):
    @unittest.skipIf(
        os.name == "nt", "POSIX recovery; disabled Windows startup is tested separately"
    )
    async def test_startup_restores_before_first_mutation_preview(self):
        plan_id = self.seed("replace:0")
        self.assertEqual((self.root / "a.py").read_bytes(), b"first = 10\r\n")
        async with self.client() as client:
            preview = await self.edit(client, self.root / "a.py", [])
            self.assertTrue(preview["no_op"])
            self.assertEqual((self.root / "a.py").read_bytes(), b"first = 1\r\n")
            self.assertEqual((self.root / "b.py").read_bytes(), b"second = 2\n")
            receipt = await self.apply(client, plan_id)
            self.assertEqual(receipt["result"]["status"], "rolled_back")
            self.assertEqual(len(receipt["result"]["files"]), 2)

    @unittest.skipIf(os.name == "nt", "POSIX recovery; Windows writes remain unsupported")
    async def test_startup_completes_committed_receipt_without_replay(self):
        plan_id = self.seed("committed")
        before = self.images()
        identity = (self.root / "a.py").stat().st_ino
        async with self.client() as client:
            receipt = await self.apply(client, plan_id)
            self.assertEqual(receipt["result"]["status"], "committed")
        self.assertEqual(before, self.images())
        self.assertEqual(identity, (self.root / "a.py").stat().st_ino)

    async def assert_locked(self, corrupt):
        plan_id = self.seed("replace:0")
        if corrupt:
            (self.state / plan_id / "journal.json").write_bytes(b"{")
        else:
            (self.root / "a.py").write_bytes(b"external = 99\n")
        before = self.images()
        async with self.client() as client:
            requests = [
                (
                    "edit_file",
                    {
                        "action": "preview",
                        "uri": (self.root / "a.py").as_uri(),
                        "edits": [],
                        "expected_hash": "0" * 64,
                    },
                ),
                (
                    "rename_symbol",
                    {
                        "action": "preview",
                        "uri": (self.root / "a.py").as_uri(),
                        "position": {"line": 0, "character": 0},
                        "new_name": "renamed",
                    },
                ),
            ] + [
                (name, {"action": "apply", "plan_id": plan_id})
                for name in ("edit_file", "rename_symbol")
            ]
            for tool, arguments in requests:
                result = await client.call_tool(tool, arguments)
                self.assertTrue(result.is_error)
                self.assertEqual(result.structured_content["error"]["code"], "RECOVERY_REQUIRED")
        self.assertEqual(before, self.images())

    @unittest.skipIf(os.name == "nt", "POSIX conflicting recovery")
    async def test_conflicting_crash_state_locks_real_preview_and_apply(self):
        await self.assert_locked(False)

    @unittest.skipIf(os.name == "nt", "POSIX corrupt recovery")
    async def test_corrupt_crash_journal_locks_real_preview_and_apply(self):
        await self.assert_locked(True)

    async def test_disabled_startup_never_restores_source(self):
        if os.name != "nt":
            plan_id = self.seed("replace:0")
        else:
            (self.root / "a.py").write_bytes(b"external = 99\n")
            plan_id = "0" * 64
            directory = self.state / plan_id
            directory.mkdir(parents=True)
            (directory / "journal.json").write_bytes(b"{")
        self.configure(enabled=False)
        before = self.images()
        journal = (self.state / plan_id / "journal.json").read_bytes()
        async with self.client() as client:
            result = await client.call_tool("edit_file", {"action": "apply", "plan_id": plan_id})
            self.assertEqual(result.structured_content["error"]["code"], "MUTATIONS_DISABLED")
        self.assertEqual(before, self.images())
        self.assertEqual((self.state / plan_id / "journal.json").read_bytes(), journal)

    @unittest.skipUnless(os.name == "nt", "Windows-specific unsupported-enabled startup control")
    async def test_windows_enabled_startup_denied_without_restoration(self):
        self.configure(enabled=True)
        (self.root / "a.py").write_bytes(b"unchanged = True\n")
        before = self.images()
        result = subprocess.run(
            [str(self.python), "-I", "-m", "gz_mcp_lsp", "--config", str(self.settings)],
            cwd=self.outside,
            input=b"",
            capture_output=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stderr)["error"]["code"], "UNSUPPORTED")
        self.assertFalse(self.state.exists())
        self.assertEqual(before, self.images())

    @unittest.skipIf(os.name == "nt", "POSIX recovery plus immediate stdin EOF")
    async def test_startup_eof_cleanup_then_restart_keeps_recovery_receipt(self):
        plan_id = self.seed("replace:0")
        result = subprocess.run(
            [str(self.python), "-I", "-m", "gz_mcp_lsp", "--config", str(self.settings)],
            cwd=self.outside,
            input=b"",
            capture_output=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", errors="replace"))
        self.assertEqual((self.root / "a.py").read_bytes(), b"first = 1\r\n")
        async with self.client() as client:
            receipt = await self.apply(client, plan_id)
            self.assertEqual(receipt["result"]["status"], "rolled_back")
