"""Installed MCP symbol extensions against provisioned, pinned real ty."""

import asyncio
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from mcp.client import Client
from mcp.client.stdio import StdioServerParameters

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.documents import Documents
from gz_mcp_lsp.models import AdapterError
from gz_mcp_lsp.navigation import Navigation
from gz_mcp_lsp.session import Session
from gz_mcp_lsp.workspace import Workspace
from tests.integration.support import install_adapter


class ActualSymbolTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.outside = Path(cls.temporary.name).resolve()
        cls.checkout = Path(__file__).resolve().parents[2]
        cls.python, cls.ty = install_adapter(cls.checkout, cls.outside)

    async def asyncSetUp(self):
        self.root = self.outside / self._testMethodName
        shutil.copytree(self.checkout / "tests/fixtures/semantic_workspace", self.root)
        self.uri = (self.root / "hierarchy.py").as_uri()
        self.settings = self.outside / (self._testMethodName + ".json")
        self.settings.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "workspace_root": str(self.root),
                    "ty_executable": str(self.ty),
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

    async def test_installed_hierarchy_duplicates_and_implementations(self):
        async with asyncio.timeout(45), self.client() as client:
            result = await client.call_tool("document_symbols", {"uri": self.uri})
            self.assertFalse(result.is_error, result.content)
            symbols = result.structured_content["result"]["symbols"]
            parent = next(item for item in symbols if item["name"] == "Parent")
            self.assertEqual(parent["selection_range"]["start"], {"line": 3, "character": 6})
            self.assertEqual(parent["range"]["start"], {"line": 3, "character": 0})
            self.assertEqual(parent["children"][0]["name"], "speak")
            self.assertEqual(
                parent["children"][0]["selection_range"]["start"], {"line": 4, "character": 8}
            )
            discovered = await client.call_tool("workspace_symbols", {"query": "speak"})
            self.assertFalse(discovered.is_error, discovered.content)
            matches = discovered.structured_content["result"]["symbols"]
            self.assertEqual(len(matches), 4)
            self.assertTrue(all(item["name"] == "speak" for item in matches))
            self.assertTrue(all(item["selection_range"] is None for item in matches))
            self.assertEqual(
                sorted(item["range"]["start"]["line"] for item in matches), [4, 9, 14, 19]
            )
            for line, character, expected in (
                (3, 6, [3, 8, 13]),
                (4, 8, [4, 9, 14]),
                (18, 6, [18]),
            ):
                implementation = await client.call_tool(
                    "implementations",
                    {"uri": self.uri, "position": {"line": line, "character": character}},
                )
                self.assertFalse(implementation.is_error, implementation.content)
                locations = implementation.structured_content["result"]["locations"]
                self.assertEqual(
                    sorted(item["range"]["start"]["line"] for item in locations), expected
                )
                self.assertTrue(all(item["uri"] == self.uri for item in locations))

    async def test_installed_empty_and_changed_workspace(self):
        shutil.rmtree(self.root)
        self.root.mkdir()
        async with asyncio.timeout(45), self.client() as client:
            empty = await client.call_tool("workspace_symbols", {"query": ""})
            self.assertFalse(empty.is_error, empty.content)
            self.assertEqual(empty.structured_content["result"]["symbols"], [])
            self.assertEqual(empty.structured_content["documents"], [])
            (self.root / "fresh.py").write_bytes(b"class FreshSymbol: pass\n")
            fresh = await client.call_tool("workspace_symbols", {"query": "FreshSymbol"})
            self.assertFalse(fresh.is_error, fresh.content)
            self.assertNotEqual(
                fresh.structured_content["workspace_generation"],
                empty.structured_content["workspace_generation"],
            )
            self.assertEqual(
                [item["name"] for item in fresh.structured_content["result"]["symbols"]],
                ["FreshSymbol"],
            )

    async def test_real_search_changed_before_final_validation(self):
        config = Config(self.root, self.ty)
        documents = Documents(Workspace(config), session := Session(config))
        await documents.start()
        async with session:
            navigation = Navigation(documents, session)
            request = session.rpc.request

            async def changed(method, params, *, timeout):
                value = await request(method, params, timeout=timeout)
                if method == "workspace/symbol":
                    (self.root / "fresh.py").write_bytes(b"class FreshSymbol: pass\n")
                return value

            with (
                patch.object(session.rpc, "request", side_effect=changed),
                self.assertRaises(AdapterError) as raised,
            ):
                await navigation.workspace_symbols("Parent")
            self.assertEqual(raised.exception.code, "STALE_DOCUMENT")
            self.assertEqual(documents.active_count, 0)
        await documents.close()
