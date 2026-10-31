"""Actual ty semantic acceptance with three callers and an independent same-name decoy."""

import json
import sys
from pathlib import Path
from typing import cast

from mcp import ClientSession, types
from mcp.client.stdio import StdioServerParameters, stdio_client

from gz_mcp_lsp.documents import Documents
from gz_mcp_lsp.models import Position
from gz_mcp_lsp.navigation import Navigation
from gz_mcp_lsp.session import Session
from gz_mcp_lsp.workspace import Workspace
from tests.integration.test_interoperability import TyFixture


class NavigationIntegration(TyFixture):
    """Inherited interoperability tests also execute under standalone discovery."""

    async def test_precise_references_match_direct_ty_and_exclude_decoy(self):
        uri = (self.root / "sample" / "runtime.py").as_uri()
        async with Session(self.config) as session:
            docs = Documents(Workspace(self.config), session)
            nav = Navigation(docs, session)
            result = await nav.references(uri, Position(3, 4))
            observed = {
                (
                    Path(item["uri"]).name,
                    item["range"]["start"]["line"],
                    item["range"]["start"]["character"],
                )
                for item in cast(dict, result["result"])["locations"]
            }
            self.assertEqual(
                observed, {("rotation.py", 2, 9), ("inventory.py", 2, 9), ("registration.py", 2, 9)}
            )
            async with docs.query(uri):
                direct = await session.rpc.request(
                    "textDocument/references",
                    {
                        "textDocument": {"uri": uri},
                        "position": {"line": 3, "character": 4},
                        "context": {"includeDeclaration": False},
                    },
                    timeout=10,
                )
                keyword = await session.rpc.request(
                    "textDocument/references",
                    {
                        "textDocument": {"uri": uri},
                        "position": {"line": 3, "character": 0},
                        "context": {"includeDeclaration": False},
                    },
                    timeout=10,
                )
            self.assertIn(keyword, [None, []])
            assert isinstance(direct, list)
            self.assertEqual(
                {item["uri"] for item in direct},
                {item["uri"] for item in cast(dict, result["result"])["locations"]},
            )
            declared = await nav.references(uri, Position(3, 4), include_declaration=True)
            self.assertIn(
                uri, {item["uri"] for item in cast(dict, declared["result"])["locations"]}
            )
            await docs.close()

    async def test_mcp_stdio_real_ty_definition_references_hover(self):
        settings = self.root.parent / "settings.json"
        settings.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "workspace_root": str(self.root),
                    "ty_executable": str(self.config.ty_executable),
                }
            )
        )
        arguments = StdioServerParameters(
            command=sys.executable, args=["-m", "gz_mcp_lsp", "--config", str(settings)]
        )
        async with (
            stdio_client(arguments) as (reader, writer),
            ClientSession(reader, writer) as client,
        ):
            await client.initialize()
            tools = await client.list_tools()
            self.assertTrue({"definition", "references", "hover"} <= {t.name for t in tools.tools})
            params = {
                "uri": (self.root / "sample" / "runtime.py").as_uri(),
                "position": {"line": 3, "character": 4},
            }
            hover = await client.call_tool("hover", params)
            self.assertFalse(hover.is_error, hover.content)
            self.assertIn("run_configured_cli", json.dumps(hover.structured_content))
            content = hover.content[0]
            assert isinstance(content, types.TextContent)
            self.assertEqual(json.loads(content.text), hover.structured_content)
            refs = await client.call_tool("references", params)
            self.assertFalse(refs.is_error)
            self.assertEqual(len(refs.structured_content["result"]["locations"]), 3)
            consumer = {
                "uri": (self.root / "sample" / "rotation.py").as_uri(),
                "position": {"line": 2, "character": 10},
            }
            definition = await client.call_tool("definition", consumer)
            self.assertFalse(definition.is_error)
            declaration = definition.structured_content["result"]["locations"][0]["declaration"]
            self.assertEqual(declaration["source_status"], "complete")
            self.assertIn("def run_configured_cli", declaration["source"])
