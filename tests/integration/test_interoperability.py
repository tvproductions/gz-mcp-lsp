"""Installed production SDK stdio to actual pinned ty: semantic content, not catalog only."""

import asyncio
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from mcp import types
from mcp.client import Client
from mcp.client.stdio import StdioServerParameters

from tests.integration.support import install_adapter


class InstalledHoverTests(unittest.IsolatedAsyncioTestCase):
    """Provision once before calls; never install anything during an MCP request."""

    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.outside = Path(cls.temporary.name).resolve()
        cls.checkout = Path(__file__).resolve().parents[2]
        cls.python, cls.ty = install_adapter(cls.checkout, cls.outside)

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
                self.assertEqual(
                    sorted(tool.name for tool in tools),
                    [
                        "definition",
                        "diagnostics",
                        "document_symbols",
                        "edit_file",
                        "hover",
                        "implementations",
                        "references",
                        "rename_symbol",
                        "workspace_symbols",
                    ],
                )
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
