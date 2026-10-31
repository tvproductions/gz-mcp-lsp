"""Real subprocess tests for protocol readiness and cleanup, without sleeps."""

import asyncio
import json
import os
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from gz_mcp_lsp.config import Config, Limits
from gz_mcp_lsp.models import AdapterError
from gz_mcp_lsp.session import Session


class SessionTests(unittest.IsolatedAsyncioTestCase):
    """A fake executable permits deterministic failure injection at the byte boundary."""

    async def asyncSetUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.executable = self.root / "fake-ty"
        source = Path(__file__).parent / "support" / "fake_lsp.py"
        self.executable.write_text(f"#!{sys.executable}\n" + source.read_text())
        self.executable.chmod(0o700)
        self.config = Config(
            self.root, self.executable, limits=replace(Limits(), shutdown_seconds=1)
        )

    async def test_initialize_once_handlers_ready_and_applyedit_denied(self):
        session = Session(self.config)
        async with session:
            await session.rpc.request("barrier", {}, timeout=1)
            events = [
                json.loads(line) for line in (self.root / "fake-events").read_text().splitlines()
            ]
            self.assertEqual(sum(e.get("method") == "initialize" for e in events), 1)
            self.assertEqual(sum(e.get("method") == "initialized" for e in events), 1)
            responses = {e["id"]: e for e in events if "result" in e}
            self.assertEqual(responses["configuration"]["result"], [None, None])
            self.assertFalse(responses["edit"]["result"]["applied"])
            init = next(e for e in events if e.get("method") == "initialize")
            self.assertEqual(
                init["params"]["capabilities"]["general"]["positionEncodings"], ["utf-16"]
            )
            child = session.process
        assert child is not None
        self.assertIsNotNone(child.returncode)
        await session.close()

    async def test_startup_failure_reaped(self):
        (self.root / "fake-mode").write_text("crash")
        session = Session(self.config)
        with self.assertRaises(AdapterError):
            await asyncio.wait_for(session.__aenter__(), 2)
        assert session.process is not None
        self.assertIsNotNone(session.process.returncode)

    async def test_shutdown_timeout_reaps_and_restart_has_only_one_child(self):
        (self.root / "fake-mode").write_text("hang-shutdown")
        session = Session(self.config)
        async with session:
            first = session.process
            await session.restart("new-generation")
            assert first is not None and session.process is not None
            self.assertIsNotNone(first.returncode)
            self.assertNotEqual(first.pid, session.process.pid)
            self.assertEqual(session.generation, "new-generation")
        assert session.process is not None
        self.assertIsNotNone(session.process.returncode)

    async def test_parent_eof_reaps_child(self):
        settings = self.root / "config.json"
        settings.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "workspace_root": str(self.root),
                    "ty_executable": str(self.executable),
                }
            )
        )
        completed = await asyncio.to_thread(
            subprocess.run,
            [sys.executable, "-m", "gz_mcp_lsp", "--config", str(settings)],
            input=b"",
            capture_output=True,
            timeout=10,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout, b"")
        child_pid = int((self.root / "fake-pid").read_text())
        with self.assertRaises(ProcessLookupError):
            os.kill(child_pid, 0)
