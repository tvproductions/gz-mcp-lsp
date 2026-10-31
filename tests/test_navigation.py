"""Precise forwarding, normalization and stable failure boundaries."""

import tempfile
import unittest
from pathlib import Path
from typing import cast

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.documents import Documents
from gz_mcp_lsp.models import AdapterError, Json, Position
from gz_mcp_lsp.navigation import Navigation
from gz_mcp_lsp.workspace import Workspace


class Peer:
    """A semantic peer records the actual position supplied by the operation."""

    def __init__(self):
        self.generation = ""
        self.capabilities: dict[str, Json] = {
            "textDocumentSync": {"openClose": True, "change": 2},
            "definitionProvider": True,
            "referencesProvider": True,
            "hoverProvider": True,
        }
        self.rpc = self
        self.calls = []
        self.response = None

    async def request(self, method, params, *, timeout):
        self.calls.append((method, params))
        return self.response

    async def restart(self, generation):
        raise AssertionError("Unexpected restart")

    async def notify(self, method, params):
        pass


class NavigationTests(unittest.IsolatedAsyncioTestCase):
    """Filesystem snapshots are real; only the semantic protocol peer is controlled."""

    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / "source.py"
        self.path.write_text("def target():\n    return 1\n")
        self.peer = Peer()
        self.docs = Documents(Workspace(Config(self.root, Path("/usr/bin/true"))), self.peer)
        self.nav = Navigation(self.docs, self.peer)

    async def test_forwarded_position_exact_and_null_hover(self):
        result = await self.nav.references(self.path.as_uri(), Position(0, 4))
        self.assertEqual(self.peer.calls[-1][1]["position"], {"line": 0, "character": 4})
        self.assertEqual(cast(dict, result["result"])["locations"], [])
        hover = await self.nav.hover(self.path.as_uri(), Position(0, 4))
        self.assertIsNone(cast(dict, hover["result"])["hover"])

    async def test_locationlink_preserves_full_and_selection_ranges(self):
        full = {"start": {"line": 0, "character": 0}, "end": {"line": 1, "character": 12}}
        selection = {"start": {"line": 0, "character": 4}, "end": {"line": 0, "character": 10}}
        self.peer.response = [
            {
                "targetUri": self.path.as_uri(),
                "targetRange": full,
                "targetSelectionRange": selection,
                "originSelectionRange": selection,
            }
        ]
        result = await self.nav.definition(self.path.as_uri(), Position(0, 4))
        target = cast(dict, result["result"])["locations"][0]
        self.assertEqual(target["range"], full)
        self.assertEqual(target["selection_range"], selection)
        self.assertEqual(target["declaration"]["source"], "def target():\n    return 1")

    async def test_external_source_metadata_only_and_limits(self):
        self.peer.response = [
            {
                "uri": "file:///outside.py",
                "range": {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 1}},
            }
        ]
        result = await self.nav.definition(self.path.as_uri(), Position(0, 4))
        self.assertEqual(
            cast(dict, result["result"])["locations"][0]["declaration"]["source_status"], "external"
        )
        with self.assertRaises(AdapterError):
            await self.nav.references(self.path.as_uri(), Position(0, 4), context_lines=21)

    async def test_locations_sort_by_numeric_coordinates(self):
        self.peer.response = [
            {
                "uri": self.path.as_uri(),
                "range": {
                    "start": {"line": line, "character": 0},
                    "end": {"line": line, "character": 1},
                },
            }
            for line in [10, 2]
        ]
        result = await self.nav.references(self.path.as_uri(), Position(0, 4))
        values = cast(dict, result["result"])["locations"]
        self.assertEqual([item["range"]["start"]["line"] for item in values], [2, 10])

    async def test_hover_variants_and_result_limit_are_not_silent_truncation(self):
        from dataclasses import replace

        for contents in (
            "type text",
            ["first", {"language": "python", "value": "int"}],
            {"kind": "markdown", "value": "```python\nint\n```"},
        ):
            self.peer.response = {"contents": contents}
            response = await self.nav.hover(self.path.as_uri(), Position(0, 4))
            self.assertEqual(cast(dict, response["result"])["hover"]["contents"], contents)
        config = self.docs.workspace.config
        self.docs.workspace.config = replace(
            config, limits=replace(config.limits, max_result_bytes=10)
        )
        with self.assertRaises(AdapterError) as failure:
            await self.nav.hover(self.path.as_uri(), Position(0, 4))
        self.assertEqual(failure.exception.code, "RESULT_LIMIT")
