"""Pinned ty and the SDK expose real hierarchy, ambiguous names and implementations."""

import json
import sys
from pathlib import Path
from typing import cast

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from gz_mcp_lsp.documents import Documents
from gz_mcp_lsp.models import Position
from gz_mcp_lsp.navigation import Navigation
from gz_mcp_lsp.session import Session
from gz_mcp_lsp.workspace import Workspace
from tests.integration.test_interoperability import TyFixture


class SymbolIntegration(TyFixture):
    """Only disposable, independently authored source is read by the real child."""

    async def test_real_ty_nested_symbols_duplicate_names_and_implementations(self):
        path = self.root / "sample" / "hierarchy.py"
        async with Session(self.config) as session:
            docs = Documents(Workspace(self.config), session)
            nav = Navigation(docs, session)
            symbols = cast(dict, (await nav.document_symbols(path.as_uri()))["result"])["symbols"]
            self.assertEqual([s["name"] for s in symbols], ["Service", "CustomService", "outer"])
            self.assertEqual(symbols[0]["range"]["start"], {"line": 0, "character": 0})
            self.assertEqual(symbols[0]["selection_range"]["start"], {"line": 0, "character": 6})
            self.assertEqual(
                symbols[0]["children"][0]["selection_range"]["start"], {"line": 1, "character": 8}
            )
            self.assertEqual(symbols[2]["children"][0]["name"], "inner")
            found = cast(dict, (await nav.workspace_symbols("run_configured_cli"))["result"])[
                "symbols"
            ]
            self.assertTrue(
                {"runtime.py", "decoy.py"} <= {Path.from_uri(s["uri"]).name for s in found}
            )
            self.assertTrue(all(s["selection_range"] is None for s in found))
            for position, expected_lines in [(Position(0, 6), {0, 5}), (Position(1, 8), {1, 6})]:
                result = cast(dict, (await nav.implementations(path.as_uri(), position))["result"])
                self.assertEqual(
                    {s["selection_range"]["start"]["line"] for s in result["locations"]},
                    expected_lines,
                )
                direct = await session.rpc.request(
                    "textDocument/implementation",
                    {
                        "textDocument": {"uri": path.as_uri()},
                        "position": {"line": position.line, "character": position.character},
                    },
                    timeout=10,
                )
                self.assertEqual(len(result["locations"]), len(cast(list, direct)))
            self.assertEqual(
                cast(dict, (await nav.workspace_symbols("no_matching_synthetic_symbol"))["result"])[
                    "symbols"
                ],
                [],
            )
            await docs.close()

    async def test_mcp_stdio_seven_read_tools_with_actual_ty(self):
        settings = self.root.parent / "settings.json"
        settings.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "workspace_root": str(self.root),
                    "ty_executable": str(self.config.ty_executable),
                }
            ),
            encoding="utf-8",
        )
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        arguments = StdioServerParameters(
            command=sys.executable, args=["-m", "gz_mcp_lsp", "--config", str(settings)]
        )
        async with (
            stdio_client(arguments) as (reader, writer),
            ClientSession(reader, writer) as client,
        ):
            await client.initialize()
            tools = await client.list_tools()
            self.assertEqual(
                {t.name for t in tools.tools},
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
            uri = (self.root / "sample" / "hierarchy.py").as_uri()
            for operation, params, field in [
                ("document_symbols", {"uri": uri}, "symbols"),
                ("workspace_symbols", {"query": "Service"}, "symbols"),
                (
                    "implementations",
                    {"uri": uri, "position": {"line": 0, "character": 6}},
                    "locations",
                ),
            ]:
                response = await client.call_tool(operation, params)
                self.assertFalse(response.is_error, response.content)
                self.assertTrue(response.structured_content["result"][field])
                self.assertEqual(response.structured_content["operation"], operation)
                self.assertTrue(response.structured_content["complete"])
            for operation in ("rename_symbol", "edit_file"):
                response = await client.call_tool(operation, {"action": "preview"})
                self.assertTrue(response.is_error)
        self.assertEqual({p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}, before)
