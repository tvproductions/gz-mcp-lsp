"""SDK composition and executable entry behavior."""

import subprocess
import sys
import unittest
from pathlib import Path

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.mcp_api import create_server
from gz_mcp_lsp.session import Session


class ApiTests(unittest.IsolatedAsyncioTestCase):
    """No semantic tool is advertised before its implementation exists."""

    async def test_intermediate_catalog_has_no_success_stubs(self):
        config = Config(Path("/tmp"), Path("/usr/bin/true"))
        server = create_server(config, Session(config))
        self.assertEqual(
            {tool.name for tool in await server.list_tools()},
            {"definition", "references", "hover", "diagnostics"},
        )

    async def test_help_and_bad_config_have_no_stdout_protocol_logs(self):
        help_reply = subprocess.run(
            [sys.executable, "-m", "gz_mcp_lsp", "--help"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        self.assertEqual(help_reply.returncode, 0)
        self.assertIn("--config", help_reply.stdout)
        invalid = subprocess.run(
            [sys.executable, "-m", "gz_mcp_lsp", "--config", "/missing-gz-config"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        self.assertNotEqual(invalid.returncode, 0)
        self.assertEqual(invalid.stdout, "")
        self.assertIn("INVALID_INPUT", invalid.stderr)

    async def test_coordinates_are_strict_at_sdk_boundary(self):
        from mcp.server.mcpserver.exceptions import ToolError

        config = Config(Path("/tmp"), Path("/usr/bin/true"))
        server = create_server(config, Session(config))
        for value in (True, 1.0, "1"):
            with self.assertRaises(ToolError):
                await server.call_tool(
                    "hover",
                    {"uri": "file:///tmp/source.py", "position": {"line": value, "character": 4}},
                )
