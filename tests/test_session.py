"""Exercise one-child lifecycle and callback order through a synthetic process."""

import asyncio
import json
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import AsyncMock, patch

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.models import AdapterError


class SessionTests(unittest.IsolatedAsyncioTestCase):
    """Own real disposable child handles, never a mocked process return code."""

    async def asyncSetUp(self):
        try:
            from gz_mcp_lsp.session import Session
        except ImportError as error:
            self.fail(f"Session lifecycle is not implemented: {error}")
        self.session_type = Session
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.record = self.root / "events.jsonl"
        self.children: list[asyncio.subprocess.Process] = []
        self.config = Config(
            self.root,
            Path(sys.executable),
            initialize_timeout_seconds=2,
            shutdown_timeout_seconds=0.1,
            kill_timeout_seconds=0.2,
        )

    def session(self, mode="normal"):
        """Substitute only process creation; exercise the actual pipes and transport."""
        peer = Path(__file__).parent / "support/fake_lsp.py"

        async def spawn(*args, **kwargs):
            self.assertEqual(args, (sys.executable, "server"))
            process = await asyncio.create_subprocess_exec(
                sys.executable, str(peer), mode, str(self.record), **kwargs
            )
            self.children.append(process)
            return process

        session = self.session_type(self.config, spawn=spawn)
        self.addAsyncCleanup(session.close)
        return session

    def events(self):
        """Read test-only lifecycle receipts after their child has closed."""
        return [json.loads(line) for line in self.record.read_text(encoding="utf-8").splitlines()]

    async def test_initialize_once_handlers_ready(self):
        """Callbacks sent during initialize complete before the single initialized notice."""
        session = self.session("early-requests")
        async with session:
            self.assertEqual(session.state, "READY")
            self.assertEqual(session.capabilities["positionEncoding"], "utf-16")
        events = self.events()
        self.assertEqual(sum(item.get("method") == "initialize" for item in events), 1)
        self.assertEqual(sum(item.get("method") == "initialized" for item in events), 1)
        configuration = next(item for item in events if item.get("reply") == "configuration")
        self.assertEqual(configuration["result"], [{}, {}])
        self.assertIsNotNone(self.children[0].returncode)

    async def test_applyedit_denied(self):
        """Unsolicited edits are rejected even if a future operator config permits writes."""
        session = self.session("early-requests")
        session.config = replace(self.config, mutations_enabled=True)
        async with session:
            pass
        reply = next(item for item in self.events() if item.get("reply") == "apply-edit")
        self.assertFalse(reply["result"]["applied"])

    async def test_startup_failure_reaped(self):
        """Failed initialize and unsupported encoding never leak a child."""
        for mode in ["exit-initialize", "bad-encoding", "hang-initialize"]:
            with self.subTest(mode=mode):
                session = self.session(mode)
                if mode == "hang-initialize":
                    session.config = replace(self.config, initialize_timeout_seconds=0.15)
                with self.assertRaises(AdapterError) as caught:
                    await session.__aenter__()
                expected = {
                    "exit-initialize": "SERVER_EXITED",
                    "bad-encoding": "UNSUPPORTED",
                    "hang-initialize": "TIMEOUT",
                }
                self.assertEqual(caught.exception.code, expected[mode])
                self.assertIsNotNone(self.children[-1].returncode)

    async def test_shutdown_timeout_and_duplicate_cleanup(self):
        """A nonresponsive shutdown is bounded and repeated close is harmless."""
        session = self.session("hang-shutdown")
        await session.__aenter__()
        await asyncio.wait_for(session.close(), 2)
        await session.close()
        self.assertEqual(session.state, "CLOSED")
        self.assertIsNotNone(self.children[0].returncode)

    async def test_stderr_flood_is_drained_and_bounded(self):
        """A full stderr pipe cannot prevent initialize or grow retained logs unboundedly."""
        session = self.session("stderr-flood")
        async with session:
            self.assertLessEqual(len(session.stderr_tail), 65536)
        self.assertIsNotNone(self.children[0].returncode)

    async def test_protocol_failure_ends_session_and_reaps(self):
        """Malformed output fails admission and eventually reaps the still-running child."""
        session = self.session()
        async with session:
            with self.assertRaises(AdapterError):
                await session.rpc.request("malformed", None, timeout=1)
            await asyncio.wait_for(session.wait_closed(), 2)
            self.assertEqual(session.state, "FAILED")
            self.assertIsNotNone(self.children[0].returncode)

    async def test_launch_error_is_a_domain_failure(self):
        """A failed exec produces a typed startup error without a traceback leak."""

        async def cannot_spawn(*args, **kwargs):
            raise OSError("invented executable failure")

        session = self.session_type(self.config, spawn=cannot_spawn)
        self.addAsyncCleanup(session.close)
        with self.assertRaises(AdapterError) as caught:
            await session.__aenter__()
        self.assertEqual(caught.exception.code, "SERVER_EXITED")
        self.assertEqual(session.state, "FAILED")

    async def test_cleanup_failure_is_not_closed_success(self):
        """A failed reap stays FAILED and still releases pending transport work."""
        session = self.session()
        await session.__aenter__()
        original_stop = session._stop_child
        task = asyncio.create_task(session.rpc.request("hold", None, timeout=5))
        while session.rpc.pending_count == 0:
            await asyncio.sleep(0)
        try:
            with (
                patch.object(
                    session,
                    "_stop_child",
                    AsyncMock(side_effect=AdapterError("SERVER_EXITED", "invented reap failure")),
                ),
                self.assertRaises(AdapterError),
            ):
                await session.close()
            self.assertEqual(session.state, "FAILED")
            with self.assertRaises(AdapterError):
                await asyncio.wait_for(task, 1)
        finally:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)
            await original_stop(False)

    async def test_restart_rejects_an_unreaped_previous_child(self):
        """A recorded cleanup failure cannot permit a second live language server."""
        session = self.session("hang-eof")
        await session.__aenter__()
        try:
            with (
                patch.object(
                    session,
                    "_stop_child",
                    AsyncMock(side_effect=AdapterError("SERVER_EXITED", "invented reap failure")),
                ),
                self.assertRaises(AdapterError),
            ):
                await session.close()
            with self.assertRaises(AdapterError):
                await session.restart("next-generation")
            self.assertEqual(len(self.children), 1)
        finally:
            for child in self.children:
                if child.returncode is None:
                    child.kill()
                await child.wait()
            await session.close()

    async def test_cancelled_startup_reaps(self):
        """Cancellation during initialize cannot leave process cleanup unfinished."""
        session = self.session("hang-initialize")
        task = asyncio.create_task(session.__aenter__())
        while not self.children:
            await asyncio.sleep(0)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertIsNotNone(self.children[0].returncode)
