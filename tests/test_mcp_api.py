"""SDK composition and executable entry behavior."""

import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from mcp import types
from mcp.server.mcpserver.exceptions import ToolError

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.mcp_api import create_server
from gz_mcp_lsp.models import AdapterError
from gz_mcp_lsp.session import Session
from tests.integration.test_interoperability import TyFixture


class ApiTests(unittest.IsolatedAsyncioTestCase):
    """No semantic tool is advertised before its implementation exists."""

    async def test_read_server_rejects_enabled_mutations_before_startup(self):
        with tempfile.TemporaryDirectory() as name:
            base = Path(name).resolve()
            root = base / "workspace"
            root.mkdir()
            source = root / "source.py"
            source.write_bytes(b"value = 1\n")
            state = base / "state"
            config = Config(
                root,
                Path("/usr/bin/true"),
                state_directory=state,
                writable_roots=(root,),
                mutations_enabled=True,
            )
            session = Session(config)
            with self.assertRaises(AdapterError) as failure:
                create_server(config, session)
            self.assertEqual(failure.exception.code, "UNSUPPORTED")
            self.assertEqual(session.state, "NEW")
            self.assertIsNone(session.process)
            self.assertFalse(state.exists())
            self.assertEqual(source.read_bytes(), b"value = 1\n")

    async def test_intermediate_catalog_has_no_success_stubs(self):
        config = Config(Path("/tmp"), Path("/usr/bin/true"))
        server = create_server(config, Session(config))
        self.assertEqual(
            {tool.name for tool in await server.list_tools()},
            {
                "definition",
                "references",
                "hover",
                "diagnostics",
                "document_symbols",
                "workspace_symbols",
                "implementations",
            },
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

    async def test_help_does_not_load_protocol_runtime(self):
        script = (
            "import sys; from gz_mcp_lsp.cli import main; "
            "exec(\"try:\\n main(['--help'])\\nexcept SystemExit:\\n pass\"); "
            "raise SystemExit(1 if 'mcp' in sys.modules else 0)"
        )
        result = subprocess.run(
            [sys.executable, "-c", script], capture_output=True, text=True, timeout=10, check=False
        )
        self.assertEqual(result.returncode, 0, result.stderr)


class ReadOnlyIntegration(TyFixture):
    """Real ty reads and denied mutation calls never acquire a filesystem writer."""

    async def test_read_server_never_initializes_transactions(self):
        state = self.root.parent / "state"
        config = replace(self.config, state_directory=state, writable_roots=(self.root,))
        before = {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        with patch(
            "gz_mcp_lsp.filesystem.Transactions.__init__",
            side_effect=AssertionError("A read operation initialized transactions"),
        ):
            session = Session(config)
            server = create_server(config, session)
            tools = await server.list_tools()
            self.assertEqual(
                {tool.name for tool in tools},
                {
                    "definition",
                    "references",
                    "hover",
                    "diagnostics",
                    "document_symbols",
                    "workspace_symbols",
                    "implementations",
                },
            )
            for tool in tools:
                self.assertIsNotNone(tool.annotations)
                assert tool.annotations is not None
                self.assertTrue(tool.annotations.read_only_hint)
                self.assertFalse(tool.annotations.destructive_hint)
            async with session:
                uri = (self.root / "sample" / "runtime.py").as_uri()
                params = {"uri": uri, "position": {"line": 3, "character": 4}}
                for operation in (
                    "definition",
                    "references",
                    "hover",
                    "diagnostics",
                    "document_symbols",
                    "workspace_symbols",
                    "implementations",
                ):
                    with self.subTest(operation=operation):
                        arguments = (
                            {"uri": uri}
                            if operation in {"diagnostics", "document_symbols"}
                            else params
                        )
                        if operation == "workspace_symbols":
                            arguments = {"query": "run_configured_cli"}
                        result = await server.call_tool(operation, arguments)
                        self.assertIsInstance(result, types.CallToolResult)
                        assert isinstance(result, types.CallToolResult)
                        self.assertFalse(result.is_error, result.content)
                        self.assertIsNotNone(result.structured_content)
                for operation in ("rename_symbol", "edit_file"):
                    with self.subTest(operation=operation), self.assertRaises(ToolError):
                        await server.call_tool(operation, {"action": "preview", **params})
        self.assertEqual(
            {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()}, before
        )
        self.assertFalse(state.exists())
        self.assertIsNotNone(session.process)
        assert session.process is not None
        self.assertIsNotNone(session.process.returncode)
