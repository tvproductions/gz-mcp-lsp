"""Exercise production SDK composition without inventing semantic stub tools."""

import unittest
from pathlib import Path
from typing import cast

from mcp.client import Client

from gz_mcp_lsp.config import Config


class StubSession:
    """Observe the lifespan boundary; real child behavior belongs to SessionTests."""

    def __init__(self):
        self.entered = False
        self.closed = False

    async def __aenter__(self):
        self.entered = True
        return self

    async def __aexit__(self, *args):
        self.closed = True


class MCPCompositionTests(unittest.IsolatedAsyncioTestCase):
    """The first composition owns SDK negotiation and exposes only implemented tools."""

    async def test_lifespan_and_empty_intermediate_catalog(self):
        """Initialize/list works without exposing unimplemented success stubs."""
        try:
            from gz_mcp_lsp.mcp_api import create_server
            from gz_mcp_lsp.session import Session
        except ImportError as error:
            self.fail(f"MCP composition is not implemented: {error}")
        session = StubSession()
        server = create_server(Config(Path.cwd(), Path(__file__)), cast("Session", session))
        async with Client(server) as client:
            self.assertTrue(session.entered)
            self.assertEqual((await client.list_tools()).tools, [])
            result = await client.session.call_tool("unimplemented", {})
            self.assertTrue(result.is_error)
        self.assertTrue(session.closed)
