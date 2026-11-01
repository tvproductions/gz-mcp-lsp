"""Installed production SDK stdio to actual pinned ty: semantic content, not catalog only."""

import asyncio
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from mcp import types
from mcp.client import Client
from mcp.client.stdio import StdioServerParameters


class InstalledHoverTests(unittest.IsolatedAsyncioTestCase):
    """Provision once before calls; never install anything during an MCP request."""

    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.outside = Path(cls.temporary.name)
        cls.checkout = Path(__file__).resolve().parents[2]
        cls.ty = Path(sys.executable).parent / ("ty.exe" if os.name == "nt" else "ty")
        if not cls.ty.is_file():
            raise AssertionError("Required pinned ty executable is missing")
        cls.prefix = cls.outside / "installed"
        cls.python = cls.prefix / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        commands = [
            ["uv", "build", "--no-sources", "--wheel", "--out-dir", str(cls.outside / "dist")],
            ["uv", "venv", "--python", sys.executable, str(cls.prefix)],
            [
                "uv",
                "export",
                "--locked",
                "--no-dev",
                "--no-emit-project",
                "--format",
                "pylock.toml",
                "--output-file",
                str(cls.outside / "pylock.toml"),
            ],
            [
                "uv",
                "pip",
                "sync",
                "--offline",
                "--python",
                str(cls.python),
                str(cls.outside / "pylock.toml"),
            ],
        ]
        for command in commands:
            result = subprocess.run(
                command,
                cwd=cls.checkout,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            if result.returncode:
                raise AssertionError(result.stderr)
        wheel = next((cls.outside / "dist").glob("*.whl"))
        result = subprocess.run(
            [
                "uv",
                "pip",
                "install",
                "--offline",
                "--no-deps",
                "--python",
                str(cls.python),
                str(wheel),
            ],
            cwd=cls.outside,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if result.returncode:
            raise AssertionError(result.stderr)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    async def test_installed_hover_and_unopened_dependency_config_visibility(self):
        """Correct identifier type changes only after a fresh child generation."""
        root = self.outside / "workspace"
        shutil.copytree(self.checkout / "tests/fixtures/semantic_workspace", root)
        expected = json.loads((root / "expected.json").read_text(encoding="utf-8"))
        settings = self.outside / "settings.json"
        settings.write_text(
            json.dumps(
                {"schema_version": 1, "workspace_root": str(root), "ty_executable": str(self.ty)}
            ),
            encoding="utf-8",
        )
        params = StdioServerParameters(
            command=str(self.python),
            args=["-I", "-m", "gz_mcp_lsp", "--config", str(settings)],
            cwd=str(self.outside),
        )
        arguments = {
            "uri": (root / expected["hover"]["uri_path"]).as_uri(),
            "position": expected["hover"]["position"],
        }
        async with asyncio.timeout(30):
            async with Client(params) as client:
                tools = (await client.list_tools()).tools
                self.assertEqual([tool.name for tool in tools], ["hover"])
                first = await client.call_tool("hover", arguments)
                self.assertFalse(first.is_error, first.content)
                before = first.structured_content
                self.assertIn("int", before["result"]["contents"]["value"])
                self.assertEqual(before["documents"][0]["uri"], arguments["uri"])
                assert isinstance(first.content[0], types.TextContent)
                self.assertEqual(json.loads(first.content[0].text), before)
                (root / "dependency.py").write_bytes(
                    b"def answer() -> str:\n    return 'changed'\n"
                )
                second = await client.call_tool("hover", arguments)
                self.assertFalse(second.is_error, second.content)
                after = second.structured_content
                self.assertIn("str", after["result"]["contents"]["value"])
                self.assertNotEqual(before["workspace_generation"], after["workspace_generation"])
                (root / "ty.toml").write_bytes(b"[environment]\npython-version = '3.13'\n")
                third = await client.call_tool("hover", arguments)
                self.assertFalse(third.is_error, third.content)
                self.assertNotEqual(
                    after["workspace_generation"], third.structured_content["workspace_generation"]
                )
