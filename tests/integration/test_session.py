"""Required actual pinned-ty startup and stdio wire checks."""

import asyncio
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from mcp.client import Client
from mcp.client.stdio import StdioServerParameters

from gz_mcp_lsp.config import Config


class ActualSessionTests(unittest.IsolatedAsyncioTestCase):
    """No skip when the project-provisioned ty executable is missing."""

    async def asyncSetUp(self):
        try:
            from gz_mcp_lsp.session import Session
        except ImportError as error:
            self.fail(f"Real-server lifecycle is not implemented: {error}")
        self.session_type = Session
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.ty = Path(sys.executable).parent / ("ty.exe" if os.name == "nt" else "ty")
        self.assertTrue(self.ty.is_file(), "Pinned ty must be provisioned before tests")

    async def test_actual_ty_initialize_and_reap(self):
        """Initialize the actual selected server and observe its child exit."""
        session = self.session_type(Config(self.root, self.ty))
        async with session:
            self.assertEqual(session.state, "READY")
            self.assertIn("textDocumentSync", session.capabilities)
            child = session.process
        self.assertIsNotNone(child.returncode)

    async def test_cli_startup_failure_is_typed_and_source_free(self):
        """A provisioned-but-invalid child reports a deliberate error without a traceback."""
        settings = self.root / "bad-child.json"
        settings.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "workspace_root": str(self.root),
                    "ty_executable": sys.executable,
                }
            ),
            encoding="utf-8",
        )
        result = await asyncio.to_thread(
            subprocess.run,
            [sys.executable, "-m", "gz_mcp_lsp", "--config", str(settings)],
            input=b"",
            capture_output=True,
            check=False,
            timeout=10,
        )
        self.assertEqual(result.returncode, 2)
        assert isinstance(result.stderr, bytes)
        self.assertTrue(result.stderr.startswith(b'{"error":'), result.stderr[:300])
        self.assertEqual(json.loads(result.stderr)["error"]["code"], "SERVER_EXITED")
        self.assertNotIn(str(self.root).encode(), result.stderr)

    async def test_stdio_no_log_bytes_and_parent_eof(self):
        """The official stdio client can negotiate/list, then close the real CLI."""
        settings = self.root / "settings.json"
        settings.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "workspace_root": str(self.root),
                    "ty_executable": str(self.ty),
                }
            ),
            encoding="utf-8",
        )
        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "gz_mcp_lsp", "--config", str(settings)],
        )
        async with asyncio.timeout(15):
            async with Client(params) as client:
                self.assertEqual(
                    sorted(tool.name for tool in (await client.list_tools()).tools),
                    [
                        "definition",
                        "diagnostics",
                        "edit_file",
                        "hover",
                        "references",
                        "rename_symbol",
                    ],
                )
        # Structured SDK parsing would fail if arbitrary log bytes entered stdout.
