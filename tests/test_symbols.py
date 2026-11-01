"""Symbol normalization and generation races through the real coordinator."""

import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from typing import cast
from unittest.mock import AsyncMock

from mcp.client import Client

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.documents import Documents
from gz_mcp_lsp.mcp_api import create_server
from gz_mcp_lsp.models import AdapterError, Position
from gz_mcp_lsp.navigation import Navigation
from gz_mcp_lsp.session import Session
from gz_mcp_lsp.workspace import Workspace
from tests.test_mcp_api import StubSession


def span(start, end):
    return {"start": {"line": 0, "character": start}, "end": {"line": 0, "character": end}}


class SymbolTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.source = self.root / "a.py"
        self.source.write_bytes(b"class A: pass\n")
        self.uri = self.source.as_uri()
        self.config = Config(self.root, self.source)
        self.session = StubSession()
        self.session.capabilities.update(
            {
                "documentSymbolProvider": True,
                "workspaceSymbolProvider": {"resolveProvider": True},
                "implementationProvider": True,
            }
        )
        self.documents = Documents(Workspace(self.config), cast("Session", self.session))
        await self.documents.start()
        self.addAsyncCleanup(self.documents.close)
        self.navigation = Navigation(self.documents, cast("Session", self.session))
        for name in ("document_symbols", "workspace_symbols", "implementations"):
            self.assertTrue(callable(getattr(self.navigation, name, None)), f"Missing {name}")

    def symbol(self, *, resolved=False):
        location = {"uri": self.uri}
        if resolved:
            location["range"] = span(6, 7)
        return {"name": "A", "kind": 5, "location": location, "data": {"key": 42}}

    async def test_nested_symbol_ranges(self):
        self.session.rpc.request = AsyncMock(
            return_value=[
                {
                    "name": "A",
                    "kind": 5,
                    "range": span(0, 13),
                    "selectionRange": span(6, 7),
                    "children": [
                        {
                            "name": "member",
                            "kind": 6,
                            "range": span(8, 12),
                            "selectionRange": span(8, 10),
                        }
                    ],
                }
            ]
        )
        result = json.loads(json.dumps(await self.navigation.document_symbols(self.uri)))
        symbol = result["result"]["symbols"][0]
        self.assertEqual(symbol["range"], span(0, 13))
        self.assertEqual(symbol["selection_range"], span(6, 7))
        self.assertEqual(symbol["children"][0]["selection_range"], span(8, 10))
        self.assertEqual(result["documents"][0]["uri"], self.uri)

    async def test_flat_document_symbols_preserve_unknown_selection(self):
        self.session.rpc.request = AsyncMock(return_value=[self.symbol(resolved=True)])
        result = json.loads(json.dumps(await self.navigation.document_symbols(self.uri)))
        symbol = result["result"]["symbols"][0]
        self.assertIsNone(symbol["selection_range"])
        self.assertEqual(symbol["range"], span(6, 7))

    async def test_uri_only_symbol_never_guesses_position(self):
        self.session.rpc.request = AsyncMock(return_value=[self.symbol()])
        result = json.loads(json.dumps(await self.navigation.workspace_symbols("A")))
        unresolved = result["result"]["symbols"][0]
        self.assertIsNone(unresolved["selection_range"])
        self.assertIsNone(unresolved["range"])
        self.assertEqual(result["documents"], [])

    async def test_duplicate_names_preserved(self):
        self.session.rpc.request = AsyncMock(return_value=[self.symbol(), self.symbol()])
        result = json.loads(json.dumps(await self.navigation.workspace_symbols("A")))
        self.assertEqual(len(result["result"]["symbols"]), 2)

    async def test_external_symbols_are_marked_without_source_access(self):
        external = self.symbol()
        external["location"] = {"uri": (self.root.parent / "external.py").as_uri()}
        self.session.rpc.request = AsyncMock(return_value=[external])
        result = json.loads(json.dumps(await self.navigation.workspace_symbols("A")))
        target = result["result"]["symbols"][0]
        self.assertEqual(target.get("source_scope"), "external")
        self.assertIsNone(target["range"])
        self.assertEqual(result["documents"], [])

    async def test_resolve_preserves_real_range_and_opaque_data(self):
        async def request(method, params, *, timeout):
            if method == "workspace/symbol":
                return [self.symbol()]
            self.assertEqual(params["data"], {"key": 42})
            return self.symbol(resolved=True)

        self.session.rpc.request = AsyncMock(side_effect=request)
        result = json.loads(json.dumps(await self.navigation.workspace_symbols("A", resolve=True)))
        symbol = result["result"]["symbols"][0]
        self.assertEqual(symbol["range"], span(6, 7))
        self.assertIsNone(symbol["selection_range"])

    async def test_resolve_without_capability_is_unsupported(self):
        self.session.capabilities["workspaceSymbolProvider"] = True
        with self.assertRaises(AdapterError) as raised:
            await self.navigation.workspace_symbols("A", resolve=True)
        self.assertEqual(raised.exception.code, "UNSUPPORTED")

    async def test_empty_workspace_symbols_needs_no_uri(self):
        self.source.unlink()
        await self.documents.start()
        self.session.rpc.request = AsyncMock(return_value=[])
        result = json.loads(json.dumps(await self.navigation.workspace_symbols("")))
        self.assertEqual(result["result"]["symbols"], [])
        self.assertEqual(self.session.rpc.notifications, [])
        self.assertEqual(self.documents.active_count, 0)

    async def race(self, phase):
        entered, release = asyncio.Event(), asyncio.Event()

        async def request(method, params, *, timeout):
            if method == phase:
                entered.set()
                await release.wait()
            return [self.symbol()] if method == "workspace/symbol" else self.symbol(resolved=True)

        self.session.rpc.request = AsyncMock(side_effect=request)
        task = asyncio.create_task(self.navigation.workspace_symbols("A", resolve=True))
        try:
            await asyncio.wait_for(entered.wait(), 10)
            self.source.write_bytes(b"class B: pass\n")
        finally:
            release.set()
        with self.assertRaises(AdapterError) as raised:
            await task
        self.assertEqual(raised.exception.code, "STALE_DOCUMENT")
        self.assertEqual(self.documents.active_count, 0)

    async def test_workspace_change_during_symbol_search(self):
        await self.race("workspace/symbol")

    async def test_workspace_change_during_symbol_resolve(self):
        await self.race("workspaceSymbol/resolve")

    async def test_implementation_supported_empty_unsupported(self):
        self.session.rpc.request = AsyncMock(return_value=None)
        result = json.loads(
            json.dumps(await self.navigation.implementations(self.uri, Position(0, 6)))
        )
        self.assertEqual(result["result"]["locations"], [])
        self.session.rpc.request = AsyncMock(
            return_value={
                "targetUri": self.uri,
                "targetRange": span(0, 13),
                "targetSelectionRange": span(6, 7),
            }
        )
        result = json.loads(
            json.dumps(await self.navigation.implementations(self.uri, Position(0, 6)))
        )
        self.assertEqual(result["result"]["locations"][0]["selection_range"], span(6, 7))
        self.session.capabilities["implementationProvider"] = False
        with self.assertRaises(AdapterError) as raised:
            await self.navigation.implementations(self.uri, Position(0, 6))
        self.assertEqual(raised.exception.code, "UNSUPPORTED")

    async def test_malformed_symbols_rejected(self):
        for symbol in (
            {"name": "bad", "kind": True},
            {"name": "bad", "kind": 5, "range": span(2, 4), "selectionRange": span(0, 1)},
        ):
            self.session.rpc.request = AsyncMock(return_value=[symbol])
            with self.assertRaises(AdapterError) as raised:
                await self.navigation.document_symbols(self.uri)
            self.assertEqual(raised.exception.code, "PROTOCOL_ERROR")

    async def test_exact_final_tool_catalog(self):
        async with Client(create_server(self.config, cast("Session", self.session))) as client:
            tools = (await client.list_tools()).tools
            self.assertEqual(
                set(tool.name for tool in tools),
                {
                    "definition",
                    "references",
                    "diagnostics",
                    "hover",
                    "rename_symbol",
                    "edit_file",
                    "document_symbols",
                    "workspace_symbols",
                    "implementations",
                },
            )
            for name, arguments in (
                ("workspace_symbols", {"query": 42}),
                ("workspace_symbols", {"query": "A", "resolve": "true"}),
                ("document_symbols", {"uri": 42}),
                ("implementations", {"uri": self.uri, "position": {"line": True, "character": 0}}),
                (
                    "implementations",
                    {"uri": self.uri, "position": {"line": 0, "character": 6}, "context_lines": 1},
                ),
            ):
                result = await client.call_tool(name, arguments)
                self.assertTrue(result.is_error)
                self.assertEqual(result.structured_content["error"]["code"], "INVALID_INPUT")
