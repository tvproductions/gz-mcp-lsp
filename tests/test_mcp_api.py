"""Actual SDK composition, strict raw arguments and production hover results."""

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import cast
from unittest.mock import AsyncMock

from mcp import types
from mcp.client import Client
from mcp.server.context import ServerRequestContext

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.session import Session
from tests.test_documents import FakeSession


class StubSession(FakeSession):
    """Observe lifecycle without changing production semantic registration."""

    def __init__(self):
        super().__init__()
        self.entered = self.closed = False
        self.capabilities["hoverProvider"] = True

    async def __aenter__(self):
        self.entered = True
        return self

    async def __aexit__(self, *args):
        self.closed = True


class MCPCompositionTests(unittest.IsolatedAsyncioTestCase):
    """The SDK exposes only the implemented production tool."""

    async def test_malformed_tool_name_delegates_to_sdk_validation(self):
        """Product middleware leaves malformed protocol envelopes to the SDK."""
        from gz_mcp_lsp.mcp_api import _strict_arguments

        context = cast(
            "ServerRequestContext", SimpleNamespace(method="tools/call", params={"name": []})
        )
        next_handler = AsyncMock(return_value=types.CallToolResult(content=[]))
        await _strict_arguments(context, next_handler)
        next_handler.assert_awaited_once_with(context)

    async def test_lifespan_schema_hover_and_strict_raw_arguments(self):
        """Typed SDK result includes equivalent JSON text; coercions are rejected."""
        from gz_mcp_lsp.mcp_api import create_server

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            source = root / "main.py"
            source.write_bytes(b"answer = 42\n")
            session = StubSession()
            session.rpc.release.set()
            server = create_server(Config(root, source), cast("Session", session))
            async with Client(server) as client:
                self.assertTrue(session.entered)
                tools = (await client.list_tools()).tools
                self.assertEqual(
                    sorted(tool.name for tool in tools),
                    ["definition", "diagnostics", "hover", "references"],
                )
                assert tools[0].annotations is not None
                self.assertTrue(tools[0].annotations.read_only_hint)
                self.assertIsNotNone(tools[0].output_schema)
                result = await client.call_tool(
                    "hover",
                    {
                        "uri": source.as_uri(),
                        "position": {"line": 0, "character": 2},
                    },
                )
                self.assertFalse(result.is_error)
                self.assertEqual(result.structured_content["operation"], "hover")
                assert isinstance(result.content[0], types.TextContent)
                self.assertEqual(json.loads(result.content[0].text), result.structured_content)
                before = len(session.rpc.notifications)
                for invalid in (
                    {"line": True, "character": 0},
                    {"line": "0", "character": 0},
                    {"line": 0.0, "character": 0},
                    '{"line":0,"character":0}',
                    {"line": 0, "character": 0, "extra": 1},
                ):
                    result = await client.call_tool(
                        "hover", {"uri": source.as_uri(), "position": invalid}
                    )
                    self.assertTrue(result.is_error)
                    self.assertEqual(result.structured_content["error"]["code"], "INVALID_INPUT")
                self.assertEqual(len(session.rpc.notifications), before)
                for name, extra in (
                    ("definition", {"context_lines": True}),
                    ("definition", {"context_lines": 21}),
                    ("references", {"include_declaration": "true"}),
                ):
                    result = await client.call_tool(
                        name,
                        {
                            "uri": source.as_uri(),
                            "position": {"line": 0, "character": 2},
                            **extra,
                        },
                    )
                    self.assertTrue(result.is_error)
                    self.assertEqual(result.structured_content["error"]["code"], "INVALID_INPUT")
                result = await client.call_tool(
                    "diagnostics",
                    {
                        "uri": source.as_uri(),
                        "context_lines": True,
                    },
                )
                self.assertTrue(result.is_error)
                self.assertEqual(result.structured_content["error"]["code"], "INVALID_INPUT")
                result = await client.call_tool("diagnostics", {"uri": source.as_uri()})
                self.assertTrue(result.is_error)
                self.assertEqual(result.structured_content["error"]["code"], "UNSUPPORTED")
            self.assertTrue(session.closed)
