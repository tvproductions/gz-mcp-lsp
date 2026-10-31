"""Real ty diagnostics after repairs and unopened dependency changes."""

import json
import sys
from typing import cast

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from gz_mcp_lsp.diagnostics import Diagnostics
from gz_mcp_lsp.documents import Documents
from gz_mcp_lsp.session import Session
from gz_mcp_lsp.workspace import Workspace
from tests.integration.test_interoperability import TyFixture


class DiagnosticIntegration(TyFixture):
    """A clean response must describe the current saved files, not a notification cache."""

    async def test_error_repair_and_dependency_change_real_ty(self):
        provider = self.root / "sample" / "provider.py"
        consumer = self.root / "sample" / "typed_consumer.py"
        provider.write_text('def promised() -> str:\n    return "okay"\n')
        consumer.write_text("from sample.provider import promised\nvalue: str = promised()\n")
        async with Session(self.config) as session:
            docs = Documents(Workspace(self.config), session)
            operation = Diagnostics(docs, session)
            initial = await operation.diagnostics(consumer.as_uri())
            self.assertEqual(cast(dict, initial["result"])["items"], [])
            before = session.generation
            provider.write_text("def promised() -> int:\n    return 1\n")
            broken = await operation.diagnostics(consumer.as_uri())
            self.assertNotEqual(session.generation, before)
            items = cast(dict, broken["result"])["items"]
            self.assertTrue(any(item["code"] == "invalid-assignment" for item in items), items)
            provider.write_text('def promised() -> str:\n    return "repaired"\n')
            repaired = await operation.diagnostics(consumer.as_uri())
            self.assertEqual(cast(dict, repaired["result"])["items"], [])
            await docs.close()

    async def test_diagnostic_mcp_stdio_actual_error_then_repair(self):
        source = self.root / "error.py"
        source.write_text('value: int = "wrong"\n')
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
        args = StdioServerParameters(
            command=sys.executable, args=["-m", "gz_mcp_lsp", "--config", str(settings)]
        )
        async with stdio_client(args) as (reader, writer), ClientSession(reader, writer) as client:
            await client.initialize()
            broken = await client.call_tool("diagnostics", {"uri": source.as_uri()})
            self.assertFalse(broken.is_error, broken.content)
            self.assertTrue(broken.structured_content["result"]["items"])
            source.write_text("value: int = 1\n")
            fixed = await client.call_tool("diagnostics", {"uri": source.as_uri()})
            self.assertFalse(fixed.is_error, fixed.content)
            self.assertEqual(fixed.structured_content["result"]["items"], [])
