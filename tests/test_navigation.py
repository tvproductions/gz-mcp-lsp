"""Production hover contracts, exact coordinates and original type text."""

import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from typing import cast
from unittest.mock import AsyncMock

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.models import AdapterError, Position
from gz_mcp_lsp.session import Session
from gz_mcp_lsp.workspace import Workspace
from tests.test_documents import FakeSession


class NavigationTests(unittest.IsolatedAsyncioTestCase):
    """Use real Documents, including final freshness validation."""

    async def asyncSetUp(self):
        try:
            from gz_mcp_lsp.documents import Documents
            from gz_mcp_lsp.navigation import Navigation
        except ImportError as error:
            self.fail(f"Hover absent: {error}")
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = self.root / "main.py"
        self.source.write_bytes(b"answer = 42\n")
        self.config = Config(self.root, self.source)
        self.session = FakeSession()
        self.session.capabilities["hoverProvider"] = True
        self.documents = Documents(Workspace(self.config), cast("Session", self.session))
        await self.documents.start()
        self.navigation = Navigation(self.documents, cast("Session", self.session))

    async def asyncTearDown(self):
        if hasattr(self, "documents"):
            await self.documents.close()

    async def test_forwarded_position_and_content(self):
        """URI and identifier coordinates survive; type text is unchanged."""
        calls = []

        async def request(method, params, *, timeout):
            calls.append((method, params))
            return {"contents": {"kind": "markdown", "value": "answer: Literal[42]"}}

        self.session.rpc.request = AsyncMock(side_effect=request)
        result = await self.navigation.hover(self.source.as_uri(), Position(0, 2))
        self.assertEqual(
            calls,
            [
                (
                    "textDocument/hover",
                    {
                        "textDocument": {"uri": self.source.as_uri()},
                        "position": {"line": 0, "character": 2},
                    },
                )
            ],
        )
        result = json.loads(json.dumps(result))
        self.assertEqual(result["result"]["contents"]["value"], "answer: Literal[42]")
        self.assertEqual(result["documents"][0]["version"], 1)
        self.assertEqual(result["documents"][0]["uri"], self.source.as_uri())
        self.assertEqual(result["schema_version"], 1)
        self.assertEqual(result["position_encoding"], "utf-16")
        self.assertTrue(result["complete"])

    async def test_invalid_position_never_sent(self):
        """Invalid offsets never become clamped or speculative requests."""
        with self.assertRaises(AdapterError) as raised:
            await self.navigation.hover(self.source.as_uri(), Position(0, 200))
        self.assertEqual(raised.exception.code, "INVALID_INPUT")
        self.assertFalse(self.session.rpc.started.is_set())

    async def test_null_is_success(self):
        """No match remains null."""

        async def request(*args, **kwargs):
            return None

        self.session.rpc.request = AsyncMock(side_effect=request)
        result = await self.navigation.hover(self.source.as_uri(), Position(0, 2))
        self.assertIsNone(result["result"])

    async def test_hover_cancellation_releases_lease(self):
        """Cancellation unwinds the held RPC context."""
        task = asyncio.create_task(self.navigation.hover(self.source.as_uri(), Position(0, 2)))
        await self.session.rpc.started.wait()
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertEqual(self.documents.active_count, 0)
