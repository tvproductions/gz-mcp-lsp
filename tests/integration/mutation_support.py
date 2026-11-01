"""Installed mutation fixture; provisioning happens only before client requests."""

import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

from mcp.client import Client
from mcp.client.stdio import StdioServerParameters

from tests.integration.support import install_adapter


class InstalledMutationCase(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(
            prefix="gz-installed-mutations-", dir=Path.home()
        )
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.outside = Path(cls.temporary.name).resolve()
        cls.checkout = Path(__file__).resolve().parents[2]
        cls.python, cls.ty = install_adapter(cls.checkout, cls.outside)

    async def asyncSetUp(self):
        self.base = self.outside / self._testMethodName
        self.base.mkdir()
        self.root = self.base / "workspace"
        self.root.mkdir(mode=0o700)
        self.state = self.base / "state"
        self.settings = self.base / "settings.json"
        self.configure(enabled=os.name != "nt")

    def configure(self, *, enabled):
        self.settings.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "workspace_root": str(self.root),
                    "ty_executable": str(self.ty),
                    "state_directory": str(self.state),
                    "mutations": {"enabled": enabled, "writable_roots": [str(self.root)]},
                }
            ),
            encoding="utf-8",
        )

    def client(self):
        return Client(
            StdioServerParameters(
                command=str(self.python),
                args=["-I", "-m", "gz_mcp_lsp", "--config", str(self.settings)],
                cwd=str(self.outside),
            )
        )

    async def call(self, client, tool, arguments) -> Any:
        response = await client.call_tool(tool, arguments)
        self.assertFalse(response.is_error, response.content)
        self.assertIsNotNone(response.structured_content)
        return response.structured_content

    async def edit(self, client, path, edits):
        return await self.call(
            client,
            "edit_file",
            {
                "action": "preview",
                "uri": path.as_uri(),
                "edits": edits,
                "expected_hash": hashlib.sha256(path.read_bytes()).hexdigest(),
            },
        )

    async def apply(self, client, plan_id, tool="edit_file"):
        return await self.call(client, tool, {"action": "apply", "plan_id": plan_id})

    def images(self):
        return {
            p.name: (p.read_bytes(), stat.S_IMODE(p.stat().st_mode))
            for p in self.root.iterdir()
            if p.is_file() and not p.is_symlink()
        }

    def seed(self, point):
        (self.root / "a.py").write_bytes(b"first = 1\r\n")
        (self.root / "b.py").write_bytes(b"second = 2\n")
        (self.root / "a.py").chmod(0o640)
        (self.root / "b.py").chmod(0o600)
        result = subprocess.run(
            [sys.executable, "-m", "tests.support.crash_transaction", str(self.base), point],
            cwd=self.checkout,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 73, result.stderr)
        return (self.base / "plan-id").read_text(encoding="ascii")
