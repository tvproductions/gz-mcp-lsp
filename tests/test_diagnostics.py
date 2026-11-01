"""Current pull diagnostics, identity-bound unchanged reports and truthful failures."""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any, cast
from unittest.mock import AsyncMock, patch

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.models import AdapterError
from gz_mcp_lsp.session import Session
from gz_mcp_lsp.workspace import Workspace
from tests.test_documents import FakeSession


class DiagnosticsTests(unittest.IsolatedAsyncioTestCase):
    """No notification cache, sleep or empty-success fallback."""

    async def asyncSetUp(self):
        try:
            from gz_mcp_lsp.diagnostics import Diagnostics
            from gz_mcp_lsp.documents import Documents
        except ImportError as error:
            self.fail(f"Pull diagnostics absent: {error}")
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.source = self.root / "main.py"
        self.dependency = self.root / "dependency.py"
        self.source.write_bytes(b"answer = 42\n")
        self.dependency.write_bytes(b"other = 1\n")
        self.session = FakeSession()
        self.session.capabilities["diagnosticProvider"] = {
            "identifier": "synthetic",
            "interFileDependencies": True,
            "workspaceDiagnostics": False,
        }
        self.documents = Documents(
            Workspace(Config(self.root, self.source)), cast("Session", self.session)
        )
        await self.documents.start()
        self.diagnostics = Diagnostics(self.documents, cast("Session", self.session))
        self.item = {
            "range": {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 6}},
            "severity": 1,
            "code": "synthetic-rule",
            "source": "ty",
            "message": "Synthetic failure",
        }

    async def asyncTearDown(self):
        if hasattr(self, "documents"):
            await self.documents.close()

    async def test_full_and_unchanged_resultid(self):
        """A valid unchanged result expands to the same full current list."""
        self.session.rpc.request = AsyncMock(
            side_effect=[
                {"kind": "full", "resultId": "one", "items": [self.item]},
                {"kind": "unchanged", "resultId": "one"},
            ]
        )
        first = json.loads(json.dumps(await self.diagnostics.diagnostics(self.source.as_uri())))
        second = json.loads(json.dumps(await self.diagnostics.diagnostics(self.source.as_uri())))
        self.assertEqual(first["result"]["items"], second["result"]["items"])
        self.assertEqual(second["result"]["items"][0]["code"], "synthetic-rule")
        self.assertEqual(second["result"]["items"][0]["severity"], 1)
        self.assertEqual(second["result"]["result_id"], "one")
        params = self.session.rpc.request.call_args.args[1]
        self.assertEqual(params["previousResultId"], "one")
        self.assertEqual(params["identifier"], "synthetic")

    async def test_unchanged_without_cache_is_protocol_error(self):
        """Unmatched unchanged reports cannot become a clean document."""
        self.session.rpc.request = AsyncMock(
            return_value={"kind": "unchanged", "resultId": "missing"}
        )
        with self.assertRaises(AdapterError) as raised:
            await self.diagnostics.diagnostics(self.source.as_uri())
        self.assertEqual(raised.exception.code, "PROTOCOL_ERROR")

    async def test_pull_error_is_not_empty_success(self):
        """RPC errors and malformed full reports fail visibly."""
        for reply in (AdapterError("TIMEOUT", "Synthetic timeout"), {"kind": "full"}, None):
            self.session.rpc.request = AsyncMock(
                side_effect=reply if isinstance(reply, Exception) else None, return_value=reply
            )
            with self.assertRaises(AdapterError) as raised:
                await self.diagnostics.diagnostics(self.source.as_uri())
            self.assertIn(raised.exception.code, {"TIMEOUT", "PROTOCOL_ERROR"})

    async def test_repair_and_dependency_change(self):
        """Document and unopened dependency changes invalidate previousResultId."""
        self.session.rpc.request = AsyncMock(
            return_value={"kind": "full", "resultId": "one", "items": [self.item]}
        )
        before = await self.diagnostics.diagnostics(self.source.as_uri())
        self.source.write_bytes(b"answer = 0\n")
        async with self.documents.generation():
            pass
        self.session.rpc.request = AsyncMock(
            return_value={"kind": "full", "resultId": "two", "items": []}
        )
        repaired = json.loads(json.dumps(await self.diagnostics.diagnostics(self.source.as_uri())))
        self.assertEqual(repaired["result"]["items"], [])
        self.assertNotIn("previousResultId", self.session.rpc.request.call_args.args[1])
        self.assertNotEqual(before["workspace_generation"], repaired["workspace_generation"])
        dependency_generation = repaired["workspace_generation"]
        self.dependency.write_bytes(b"other = 'changed'\n")
        async with self.documents.generation():
            pass
        self.session.rpc.request = AsyncMock(
            return_value={"kind": "full", "resultId": "three", "items": [self.item]}
        )
        changed = await self.diagnostics.diagnostics(self.source.as_uri())
        self.assertNotEqual(dependency_generation, changed["workspace_generation"])
        self.assertNotIn("previousResultId", self.session.rpc.request.call_args.args[1])

    async def test_cached_items_are_not_mutated_by_a_caller(self):
        """Returned JSON cannot poison a later unchanged report."""
        self.session.rpc.request = AsyncMock(
            side_effect=[
                {"kind": "full", "resultId": "one", "items": [copy.deepcopy(self.item)]},
                {"kind": "unchanged", "resultId": "one"},
            ]
        )
        first = cast("dict[str, Any]", await self.diagnostics.diagnostics(self.source.as_uri()))
        first["result"]["items"][0]["message"] = "poison"
        second = cast("dict[str, Any]", await self.diagnostics.diagnostics(self.source.as_uri()))
        self.assertEqual(second["result"]["items"][0]["message"], "Synthetic failure")

    async def test_related_full_and_unchanged_reports_keep_identity(self):
        """Related local reports need their own saved hash/generation and resultId."""
        related_uri = self.dependency.as_uri()
        self.session.rpc.request = AsyncMock(
            side_effect=[
                {
                    "kind": "full",
                    "resultId": "main",
                    "items": [],
                    "relatedDocuments": {
                        related_uri: {"kind": "full", "resultId": "related", "items": [self.item]}
                    },
                },
                {
                    "kind": "unchanged",
                    "resultId": "main",
                    "relatedDocuments": {related_uri: {"kind": "unchanged", "resultId": "related"}},
                },
            ]
        )
        first = json.loads(json.dumps(await self.diagnostics.diagnostics(self.source.as_uri())))
        second = json.loads(json.dumps(await self.diagnostics.diagnostics(self.source.as_uri())))
        self.assertEqual(first["result"], second["result"])
        self.assertEqual(second["result"]["related_documents"][0]["items"][0]["uri"], related_uri)
        self.assertEqual(len(second["documents"]), 2)

    async def test_mismatched_resultid_and_unsupported_provider_fail(self):
        """An arbitrary new unchanged token cannot reuse an older full list."""
        self.session.rpc.request = AsyncMock(
            side_effect=[
                {"kind": "full", "resultId": "one", "items": [self.item]},
                {"kind": "unchanged", "resultId": "different"},
            ]
        )
        await self.diagnostics.diagnostics(self.source.as_uri())
        with self.assertRaises(AdapterError) as raised:
            await self.diagnostics.diagnostics(self.source.as_uri())
        self.assertEqual(raised.exception.code, "PROTOCOL_ERROR")
        self.session.capabilities.pop("diagnosticProvider")
        self.session.rpc.request.reset_mock()
        with self.assertRaises(AdapterError) as raised:
            await self.diagnostics.diagnostics(self.source.as_uri())
        self.assertEqual(raised.exception.code, "UNSUPPORTED")
        self.session.rpc.request.assert_not_awaited()

    async def test_context_is_not_cached_as_current_diagnostic_data(self):
        """Each call chooses fresh context formatting around the same current base report."""
        self.session.rpc.request = AsyncMock(
            side_effect=[
                {"kind": "full", "resultId": "one", "items": [self.item]},
                {"kind": "unchanged", "resultId": "one"},
            ]
        )
        first = json.loads(json.dumps(await self.diagnostics.diagnostics(self.source.as_uri(), 1)))
        second = json.loads(json.dumps(await self.diagnostics.diagnostics(self.source.as_uri(), 0)))
        self.assertIn("context", first["result"]["items"][0])
        self.assertNotIn("context", second["result"]["items"][0])

    async def test_related_external_documents_are_metadata_only(self):
        """A returned external report cannot trigger an external source read."""
        external = (self.root.parent / "outside.py").as_uri()
        self.session.rpc.request = AsyncMock(
            return_value={
                "kind": "full",
                "items": [],
                "relatedDocuments": {
                    external: {"kind": "full", "resultId": "external", "items": [self.item]},
                },
            }
        )
        original = self.documents.workspace.read

        def read(uri):
            self.assertNotEqual(uri, external)
            return original(uri)

        with patch.object(self.documents.workspace, "read", side_effect=read):
            result = json.loads(
                json.dumps(await self.diagnostics.diagnostics(self.source.as_uri()))
            )
        self.assertEqual(result["result"]["related_documents"][0]["source_scope"], "external")
        self.assertEqual(
            result["documents"],
            [
                {
                    "uri": self.source.as_uri(),
                    "sha256": self.documents.workspace.read(self.source.as_uri()).sha256,
                    "version": 1,
                }
            ],
        )
