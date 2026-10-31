"""Current pull reports, trustworthy unchanged cache and explicit failures."""

from typing import cast

from test_navigation import NavigationFixture

from gz_mcp_lsp.diagnostics import Diagnostics
from gz_mcp_lsp.models import AdapterError


class DiagnosticTests(NavigationFixture):
    """Reuse semantic setup while exercising pull report contracts."""

    async def test_full_and_unchanged_resultid(self):
        self.peer.capabilities["diagnosticProvider"] = {"interFileDependencies": True}
        operation = Diagnostics(self.docs, self.peer)
        diagnostic = {
            "range": {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 3}},
            "severity": 1,
            "code": "test-code",
            "source": "ty",
            "message": "synthetic",
        }
        self.peer.response = {"kind": "full", "resultId": "one", "items": [diagnostic]}
        first = await operation.diagnostics(self.path.as_uri())
        self.peer.response = {"kind": "unchanged", "resultId": "one"}
        second = await operation.diagnostics(self.path.as_uri())
        self.assertEqual(
            cast(dict, first["result"])["items"], cast(dict, second["result"])["items"]
        )
        self.assertEqual(self.peer.calls[-1][1]["previousResultId"], "one")

    async def test_unmatched_unchanged_and_pull_error_not_empty_success(self):
        self.peer.capabilities["diagnosticProvider"] = True
        operation = Diagnostics(self.docs, self.peer)
        self.peer.response = {"kind": "unchanged", "resultId": "unknown"}
        with self.assertRaises(AdapterError) as failure:
            await operation.diagnostics(self.path.as_uri())
        self.assertEqual(failure.exception.code, "PROTOCOL_ERROR")
        self.peer.response = None
        with self.assertRaises(AdapterError):
            await operation.diagnostics(self.path.as_uri())

    async def test_generation_cache_is_invalidated(self):
        self.peer.capabilities["diagnosticProvider"] = True
        operation = Diagnostics(self.docs, self.peer)
        self.peer.response = {"kind": "full", "resultId": "one", "items": []}
        await operation.diagnostics(self.path.as_uri())
        self.path.write_text("def target():\n    return 2\n")
        self.peer.response = {"kind": "unchanged", "resultId": "one"}
        with self.assertRaises(AdapterError):
            await operation.diagnostics(self.path.as_uri())
