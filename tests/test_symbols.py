"""Public symbol discovery retains ambiguity and never manufactures identifier ranges."""

import json
import unittest
from dataclasses import replace
from typing import cast
from unittest.mock import patch

from mcp.server.mcpserver.exceptions import ToolError

from gz_mcp_lsp.mcp_api import create_server
from gz_mcp_lsp.models import AdapterError, Position
from gz_mcp_lsp.session import Session
from tests.test_navigation import NavigationFixture
from tests.test_session import ProcessFixture


def span(start_line, start_column, end_line, end_column):
    return {
        "start": {"line": start_line, "character": start_column},
        "end": {"line": end_line, "character": end_column},
    }


class SymbolsTests(NavigationFixture):
    """Only the protocol peer is controlled; saved-document generations are real."""

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.peer.capabilities.update(
            documentSymbolProvider=True, workspaceSymbolProvider=True, implementationProvider=True
        )

    async def call(self, operation, *args, **kwargs):
        method = getattr(self.nav, operation, None)
        self.assertTrue(callable(method), f"Missing public operation: {operation}")
        assert callable(method)
        return cast(dict, (await method(*args, **kwargs))["result"])

    async def test_nested_symbol_ranges(self):
        full, selected = span(0, 0, 1, 12), span(0, 4, 0, 10)
        self.peer.response = [
            {
                "name": "outer",
                "kind": 12,
                "detail": "outer detail",
                "range": full,
                "selectionRange": selected,
                "children": [
                    {
                        "name": "inner",
                        "kind": 12,
                        "range": span(1, 4, 1, 12),
                        "selectionRange": span(1, 4, 1, 10),
                        "tags": [1],
                    }
                ],
            }
        ]
        symbols = (await self.call("document_symbols", self.path.as_uri()))["symbols"]
        self.assertEqual(symbols[0]["range"], full)
        self.assertEqual(symbols[0]["selection_range"], selected)
        self.assertEqual(symbols[0]["detail"], "outer detail")
        self.assertEqual(symbols[0]["children"][0]["name"], "inner")
        self.assertEqual(symbols[0]["children"][0]["tags"], [1])
        self.assertEqual(
            self.peer.calls[-1],
            ("textDocument/documentSymbol", {"textDocument": {"uri": self.path.as_uri()}}),
        )

    async def test_flat_document_symbols_have_no_invented_selection(self):
        self.peer.response = [
            {
                "name": "target",
                "kind": 12,
                "containerName": "module",
                "location": {"uri": self.path.as_uri(), "range": span(0, 0, 1, 12)},
            }
        ]
        symbol = (await self.call("document_symbols", self.path.as_uri()))["symbols"][0]
        self.assertIsNone(symbol["selection_range"])
        self.assertEqual(symbol["container_name"], "module")

    async def test_uri_only_symbol_never_guesses_position(self):
        self.peer.response = [
            {
                "name": "target",
                "kind": 12,
                "location": {"uri": self.path.as_uri()},
                "data": {"token": 7},
            }
        ]
        symbol = (await self.call("workspace_symbols", "target"))["symbols"][0]
        self.assertIsNone(symbol["range"])
        self.assertIsNone(symbol["selection_range"])
        self.assertFalse(symbol["resolved"])
        self.assertEqual(self.peer.calls, [("workspace/symbol", {"query": "target"})])
        with self.assertRaises(AdapterError) as failure:
            await self.call("workspace_symbols", "target", resolve=True)
        self.assertEqual(failure.exception.code, "UNSUPPORTED")

    async def test_workspace_resolution_preserves_opaque_request_and_range_distinction(self):
        original = {
            "name": "target",
            "kind": 12,
            "location": {"uri": self.path.as_uri()},
            "data": {"token": 7},
        }
        resolved = original | {"location": {"uri": self.path.as_uri(), "range": span(0, 0, 1, 12)}}
        self.peer.capabilities["workspaceSymbolProvider"] = {"resolveProvider": True}

        async def request(method, params, *, timeout):
            self.peer.calls.append((method, params))
            return [original] if method == "workspace/symbol" else resolved

        with patch.object(self.peer, "request", side_effect=request):
            symbol = (await self.call("workspace_symbols", "target", resolve=True))["symbols"][0]
        self.assertTrue(symbol["resolved"])
        self.assertEqual(symbol["range"], span(0, 0, 1, 12))
        self.assertIsNone(symbol["selection_range"])
        self.assertEqual(self.peer.calls[-1], ("workspaceSymbol/resolve", original))
        self.assertNotIn("range", original["location"])

    async def test_duplicate_names_preserved_and_sorted_by_numeric_position(self):
        self.peer.response = [
            {
                "name": "duplicate",
                "kind": 12,
                "location": {"uri": self.path.as_uri(), "range": span(line, 0, line, 9)},
            }
            for line in [10, 2]
        ]
        symbols = (await self.call("workspace_symbols", "duplicate"))["symbols"]
        self.assertEqual(len(symbols), 2)
        self.assertEqual([s["name"] for s in symbols], ["duplicate", "duplicate"])
        self.assertEqual([s["range"]["start"]["line"] for s in symbols], [2, 10])
        self.assertTrue(all(s["selection_range"] is None for s in symbols))

    async def test_resolution_can_change_sort_order_without_changing_identity(self):
        self.peer.capabilities["workspaceSymbolProvider"] = {"resolveProvider": True}
        original = [
            {"name": name, "kind": 12, "location": {"uri": self.path.as_uri()}, "data": line}
            for name, line in [("alpha", 10), ("zeta", 2)]
        ]

        async def request(method, params, *, timeout):
            if method == "workspace/symbol":
                return original
            return params | {
                "location": {
                    "uri": self.path.as_uri(),
                    "range": span(params["data"], 0, params["data"], 4),
                }
            }

        with patch.object(self.peer, "request", side_effect=request):
            found = (await self.call("workspace_symbols", "", resolve=True))["symbols"]
        self.assertEqual([s["name"] for s in found], ["zeta", "alpha"])

    async def test_strict_symbol_inputs_at_sdk_boundary(self):
        config = self.docs.workspace.config
        server = create_server(config, Session(config))
        for arguments in [{"query": True}, {"query": "target", "resolve": 1}]:
            with self.subTest(arguments=arguments), self.assertRaises(ToolError):
                await server.call_tool("workspace_symbols", arguments)

    async def test_resolution_rejects_changed_symbol_identity(self):
        self.peer.capabilities["workspaceSymbolProvider"] = {"resolveProvider": True}
        original = {"name": "target", "kind": 12, "location": {"uri": self.path.as_uri()}}
        for changes in [
            {"name": "other"},
            {"kind": 5},
            {"location": {"uri": "file:///external.py", "range": span(0, 0, 0, 1)}},
        ]:

            async def request(method, params, *, timeout, change=changes):
                return [original] if method == "workspace/symbol" else original | change

            with (
                self.subTest(changes=changes),
                patch.object(self.peer, "request", side_effect=request),
            ):
                with self.assertRaises(AdapterError) as failure:
                    await self.call("workspace_symbols", "target", resolve=True)
                self.assertEqual(failure.exception.code, "PROTOCOL_ERROR")

    async def test_symbol_queries_reject_concurrent_saved_changes(self):
        for index, (operation, arguments) in enumerate(
            [
                ("document_symbols", (self.path.as_uri(),)),
                ("workspace_symbols", ("target",)),
                ("implementations", (self.path.as_uri(), Position(0, 4))),
            ]
        ):

            async def request(method, params, *, timeout, number=index):
                self.path.write_bytes(f"value = {number}\n".encode())
                return []

            with (
                self.subTest(operation=operation),
                patch.object(self.peer, "request", side_effect=request),
            ):
                with self.assertRaises(AdapterError) as failure:
                    await self.call(operation, *arguments)
                self.assertEqual(failure.exception.code, "STALE_DOCUMENT")
                self.assertFalse(self.docs.lock.locked())

    async def test_implementation_supported_empty_unsupported(self):
        self.assertEqual(
            (await self.call("implementations", self.path.as_uri(), Position(0, 4)))["locations"],
            [],
        )
        self.peer.response = [
            {
                "targetUri": self.path.as_uri(),
                "targetRange": span(0, 0, 1, 12),
                "targetSelectionRange": span(0, 4, 0, 10),
            }
        ]
        found = (await self.call("implementations", self.path.as_uri(), Position(0, 4)))[
            "locations"
        ]
        self.assertEqual(found[0]["selection_range"], span(0, 4, 0, 10))
        self.assertEqual(self.peer.calls[-1][1]["position"], {"line": 0, "character": 4})
        self.peer.capabilities["implementationProvider"] = False
        with self.assertRaises(AdapterError) as failure:
            await self.call("implementations", self.path.as_uri(), Position(0, 4))
        self.assertEqual(failure.exception.code, "UNSUPPORTED")

    async def test_symbols_capabilities_and_result_limits(self):
        for operation, capability, arguments in [
            ("document_symbols", "documentSymbolProvider", (self.path.as_uri(),)),
            ("workspace_symbols", "workspaceSymbolProvider", ("query",)),
        ]:
            with self.subTest(operation=operation):
                self.peer.capabilities[capability] = False
                with self.assertRaises(AdapterError) as failure:
                    await self.call(operation, *arguments)
                self.assertEqual(failure.exception.code, "UNSUPPORTED")
                self.peer.capabilities[capability] = True
        config = self.docs.workspace.config
        self.docs.workspace.config = replace(
            config, limits=replace(config.limits, max_result_bytes=10)
        )
        for operation, arguments in [
            ("document_symbols", (self.path.as_uri(),)),
            ("workspace_symbols", ("query",)),
            ("implementations", (self.path.as_uri(), Position(0, 4))),
        ]:
            with self.subTest(operation=operation):
                with self.assertRaises(AdapterError) as failure:
                    await self.call(operation, *arguments)
                self.assertEqual(failure.exception.code, "RESULT_LIMIT")

    async def test_malformed_symbols_fail_protocol_validation(self):
        for symbol in [
            {
                "name": "bad",
                "kind": True,
                "range": span(0, 0, 1, 12),
                "selectionRange": span(0, 4, 0, 10),
            },
            {
                "name": "bad",
                "kind": 12,
                "range": span(0, 0, 0, 3),
                "selectionRange": span(0, 4, 0, 10),
            },
            {
                "name": "bad",
                "kind": 12,
                "range": span(0, 0, 1, 12),
                "selectionRange": span(0, 4, 0, 10),
                "children": "bad",
            },
            {"name": "bad", "kind": 12, "location": {"uri": self.path.as_uri()}},
        ]:
            self.peer.response = [symbol]
            with self.subTest(symbol=symbol):
                with self.assertRaises(AdapterError) as failure:
                    await self.call("document_symbols", self.path.as_uri())
                self.assertEqual(failure.exception.code, "PROTOCOL_ERROR")

    async def test_exact_read_tool_catalog(self):
        config = self.docs.workspace.config
        server = create_server(config, Session(config))
        tools = await server.list_tools()
        self.assertEqual(
            {t.name for t in tools},
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
        for operation in ("rename_symbol", "edit_file"):
            with self.assertRaises(ToolError):
                await server.call_tool(operation, {})


class SymbolCapabilitiesTests(ProcessFixture):
    """URI-only workspace symbols are negotiated explicitly on the actual LSP wire."""

    async def test_workspace_resolution_is_advertised(self):
        async with Session(self.config) as session:
            await session.rpc.request("barrier", {}, timeout=1)
            events = [
                json.loads(line) for line in (self.root / "fake-events").read_text().splitlines()
            ]
            init = next(e for e in events if e.get("method") == "initialize")
            symbols = init["params"]["capabilities"]["workspace"].get("symbol", {})
            self.assertEqual(symbols.get("resolveSupport"), {"properties": ["location.range"]})


if __name__ == "__main__":
    unittest.main()
