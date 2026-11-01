"""Production hover contracts, exact coordinates and original type text."""

import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from typing import cast
from unittest.mock import AsyncMock

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.models import AdapterError, Position
from gz_mcp_lsp.session import Session
from gz_mcp_lsp.workspace import Workspace
from tests.test_documents import FakeSession


class NavigationTests(unittest.IsolatedAsyncioTestCase):
    """Use real Documents, including final freshness validation."""

    async def asyncSetUp(self):
        try:
            from gz_mcp_lsp.documents import Documents
            from gz_mcp_lsp.navigation import Navigation
        except ImportError as error:
            self.fail(f"Hover absent: {error}")
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = self.root / "main.py"
        self.source.write_bytes(b"answer = 42\n")
        self.config = Config(self.root, self.source)
        self.session = FakeSession()
        self.session.capabilities["hoverProvider"] = True
        self.documents = Documents(Workspace(self.config), cast("Session", self.session))
        await self.documents.start()
        self.navigation = Navigation(self.documents, cast("Session", self.session))

    async def asyncTearDown(self):
        if hasattr(self, "documents"):
            await self.documents.close()

    async def test_forwarded_position_and_content(self):
        """URI and identifier coordinates survive; type text is unchanged."""
        calls = []

        async def request(method, params, *, timeout):
            calls.append((method, params))
            return {"contents": {"kind": "markdown", "value": "answer: Literal[42]"}}

        self.session.rpc.request = AsyncMock(side_effect=request)
        result = await self.navigation.hover(self.source.as_uri(), Position(0, 2))
        self.assertEqual(
            calls,
            [
                (
                    "textDocument/hover",
                    {
                        "textDocument": {"uri": self.source.as_uri()},
                        "position": {"line": 0, "character": 2},
                    },
                )
            ],
        )
        result = json.loads(json.dumps(result))
        self.assertEqual(result["result"]["contents"]["value"], "answer: Literal[42]")
        self.assertEqual(result["documents"][0]["version"], 1)
        self.assertEqual(result["documents"][0]["uri"], self.source.as_uri())
        self.assertEqual(result["schema_version"], 1)
        self.assertEqual(result["position_encoding"], "utf-16")
        self.assertTrue(result["complete"])

    async def test_invalid_position_never_sent(self):
        """Invalid offsets never become clamped or speculative requests."""
        with self.assertRaises(AdapterError) as raised:
            await self.navigation.hover(self.source.as_uri(), Position(0, 200))
        self.assertEqual(raised.exception.code, "INVALID_INPUT")
        self.assertFalse(self.session.rpc.started.is_set())

    async def test_null_is_success(self):
        """No match remains null."""

        async def request(*args, **kwargs):
            return None

        self.session.rpc.request = AsyncMock(side_effect=request)
        result = await self.navigation.hover(self.source.as_uri(), Position(0, 2))
        self.assertIsNone(result["result"])

    async def test_hover_cancellation_releases_lease(self):
        """Cancellation unwinds the held RPC context."""
        task = asyncio.create_task(self.navigation.hover(self.source.as_uri(), Position(0, 2)))
        await self.session.rpc.started.wait()
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertEqual(self.documents.active_count, 0)

    async def test_forwarded_position_is_exact(self):
        """One-line definition caller coordinates are never shifted by a keyword length."""
        self.source.write_bytes(b"def item(): pass\n")
        await self.documents.start()
        self.session.capabilities.update({"definitionProvider": True, "referencesProvider": True})
        self.session.rpc.request = AsyncMock(return_value=None)
        await self.navigation.definition(self.source.as_uri(), Position(0, 4))
        sent_params = self.session.rpc.request.call_args.args[1]
        self.assertEqual(sent_params["position"], {"line": 0, "character": 4})
        self.assertEqual(sent_params["textDocument"]["uri"], self.source.as_uri())

    async def test_locationlink_ranges_remain_distinct(self):
        """Origin, target full range and target identifier range remain separate."""
        self.session.capabilities.update(
            {"definitionProvider": True, "documentSymbolProvider": True}
        )
        full = {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 11}}
        selection = {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 6}}
        origin = {"start": {"line": 0, "character": 1}, "end": {"line": 0, "character": 3}}

        async def request(method, params, *, timeout):
            if method == "textDocument/definition":
                return [
                    {
                        "targetUri": self.source.as_uri(),
                        "targetRange": full,
                        "targetSelectionRange": selection,
                        "originSelectionRange": origin,
                    }
                ]
            if method == "textDocument/documentSymbol":
                return []
            raise AssertionError(method)

        self.session.rpc.request = AsyncMock(side_effect=request)
        result = json.loads(
            json.dumps(await self.navigation.definition(self.source.as_uri(), Position(0, 2)))
        )
        target = result["result"]["locations"][0]
        self.assertEqual(target["range"], full)
        self.assertEqual(target["selection_range"], selection)
        self.assertEqual(target["origin_selection_range"], origin)
        self.assertEqual(target["source"]["text"], "answer = 42")
        self.assertEqual(self.documents.active_count, 0)

    async def test_external_source_not_read(self):
        """External definition metadata never causes an external snapshot or symbol query."""
        external = (self.root.parent / "must-not-open.py").as_uri()
        self.session.capabilities["definitionProvider"] = True
        extent = {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 4}}
        self.session.rpc.request = AsyncMock(return_value={"uri": external, "range": extent})
        original = self.documents.workspace.read

        def read(uri):
            self.assertNotEqual(uri, external)
            return original(uri)

        from unittest.mock import patch

        with patch.object(self.documents.workspace, "read", side_effect=read):
            result = json.loads(
                json.dumps(await self.navigation.definition(self.source.as_uri(), Position(0, 2)))
            )
        target = result["result"]["locations"][0]
        self.assertEqual(target["source_scope"], "external")
        self.assertIsNone(target["source"])
        self.assertEqual(self.session.rpc.request.await_count, 1)

    async def test_references_order_context_and_flag(self):
        """Reference order is deterministic and the declaration flag is forwarded exactly."""
        self.session.capabilities["referencesProvider"] = True
        first = {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 1}}
        second = {"start": {"line": 0, "character": 2}, "end": {"line": 0, "character": 3}}
        self.session.rpc.request = AsyncMock(
            return_value=[
                {"uri": self.source.as_uri(), "range": second},
                {"uri": self.source.as_uri(), "range": first},
            ]
        )
        result = json.loads(
            json.dumps(
                await self.navigation.references(
                    self.source.as_uri(), Position(0, 2), include_declaration=True, context_lines=1
                )
            )
        )
        sent = self.session.rpc.request.call_args.args[1]
        self.assertEqual(sent["context"], {"includeDeclaration": True})
        items = result["result"]["locations"]
        self.assertEqual([item["range"] for item in items], [first, second])
        self.assertEqual(items[0]["context"]["text"], "answer = 42\n")

    async def test_source_budget_stops_before_reading_all_targets(self):
        """Growing source attachments must fail before materializing an oversized whole set."""
        from dataclasses import replace

        from gz_mcp_lsp.config import Limits

        self.source.write_bytes(("answer = '" + "x" * 400 + "'\n").encode())
        self.documents.workspace.config = replace(self.config, limits=Limits(result_bytes=2500))
        await self.documents.start()
        self.session.capabilities["definitionProvider"] = True
        extent = {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 6}}
        self.session.rpc.request = AsyncMock(
            return_value=[{"uri": self.source.as_uri(), "range": extent} for _ in range(4)]
        )
        self.navigation._source = AsyncMock(wraps=self.navigation._source)
        with self.assertRaises(AdapterError) as raised:
            await self.navigation.definition(self.source.as_uri(), Position(0, 2))
        self.assertEqual(raised.exception.code, "RESULT_LIMIT")
        self.assertLess(self.navigation._source.await_count, 4)

    async def test_external_reference_metadata_without_context(self):
        """External references remain marked even when no source context was requested."""
        self.session.capabilities["referencesProvider"] = True
        extent = {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 4}}
        self.session.rpc.request = AsyncMock(
            return_value=[{"uri": "https://example.invalid/external.py", "range": extent}]
        )
        result = json.loads(
            json.dumps(await self.navigation.references(self.source.as_uri(), Position(0, 2)))
        )
        target = result["result"]["locations"][0]
        self.assertEqual(target["source_scope"], "external")
        self.assertIsNone(target["source"])

    async def test_null_hover_variants(self):
        """Each legal original form survives without type-text normalization."""
        variants = [
            None,
            {"contents": "plain"},
            {"contents": {"language": "python", "value": "answer: int"}},
            {"contents": [{"language": "python", "value": "answer: int"}, "doc"]},
            {"contents": {"kind": "markdown", "value": "**answer**"}},
        ]
        for value in variants:
            self.session.rpc.request = AsyncMock(return_value=value)
            result = await self.navigation.hover(self.source.as_uri(), Position(0, 2))
            self.assertEqual(result["result"], value)
        self.session.rpc.request = AsyncMock(
            return_value={"contents": {"kind": [], "value": "malformed"}}
        )
        with self.assertRaises(AdapterError) as raised:
            await self.navigation.hover(self.source.as_uri(), Position(0, 2))
        self.assertEqual(raised.exception.code, "PROTOCOL_ERROR")
