"""Installed pull diagnostics must follow saved repairs and unopened dependency edits."""

import asyncio
import json
import tempfile
import unittest
from pathlib import Path

from mcp.client import Client
from mcp.client.stdio import StdioServerParameters

from tests.integration.support import install_adapter


class ActualDiagnosticTests(unittest.IsolatedAsyncioTestCase):
    """Actual pinned ty, no skip/sleep/push cache and no request-time installation."""

    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.outside = Path(cls.temporary.name)
        cls.checkout = Path(__file__).resolve().parents[2]
        cls.python, cls.ty = install_adapter(cls.checkout, cls.outside)

    async def asyncSetUp(self):
        self.root = self.outside / self._testMethodName
        self.root.mkdir()
        self.cases = json.loads(
            (self.checkout / "tests/fixtures/diagnostic_cases.json").read_text(encoding="utf-8")
        )
        self.source = self.root / "error.py"
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

    async def test_error_repair_and_current_full_result(self):
        """A true pull reports the expected error; a saved fix produces a fresh empty list."""
        self.source.write_text(self.cases["error_source"], encoding="utf-8", newline="")
        async with asyncio.timeout(40):
            async with self.client() as client:
                first = await client.call_tool(
                    "diagnostics", {"uri": self.source.as_uri(), "context_lines": 1}
                )
                self.assertFalse(first.is_error, first.content)
                before = first.structured_content
                items = before["result"]["items"]
                self.assertEqual(len(items), 1)
                self.assertEqual(items[0]["uri"], self.source.as_uri())
                self.assertEqual(items[0]["range"], self.cases["expected"]["error_range"])
                self.assertEqual(items[0]["code"], self.cases["expected"]["code"])
                self.assertEqual(items[0]["source"], "ty")
                self.assertEqual(items[0]["severity"], self.cases["expected"]["severity"])
                self.assertIn("int", items[0]["message"])
                self.assertEqual(items[0]["context"]["text"], self.cases["error_source"])
                again = await client.call_tool(
                    "diagnostics", {"uri": self.source.as_uri(), "context_lines": 1}
                )
                self.assertFalse(again.is_error, again.content)
                self.assertEqual(again.structured_content["result"]["items"], items)
                self.source.write_text(self.cases["repair_source"], encoding="utf-8", newline="")
                result = await client.call_tool("diagnostics", {"uri": self.source.as_uri()})
                self.assertFalse(result.is_error, result.content)
                repaired = result.structured_content
                self.assertEqual(repaired["result"]["items"], [])
                self.assertNotEqual(
                    before["workspace_generation"], repaired["workspace_generation"]
                )

    async def test_unopened_dependency_changes_consumer_diagnostics(self):
        """A clean consumer becomes erroneous after only the unopened dependency changes."""
        self.source.write_text(self.cases["consumer_source"], encoding="utf-8", newline="")
        dependency = self.root / "diagnostic_dependency.py"
        dependency.write_text(self.cases["dependency_source"], encoding="utf-8", newline="")
        async with asyncio.timeout(40):
            async with self.client() as client:
                first = await client.call_tool("diagnostics", {"uri": self.source.as_uri()})
                self.assertFalse(first.is_error, first.content)
                self.assertEqual(first.structured_content["result"]["items"], [])
                dependency_generation = first.structured_content["workspace_generation"]
                dependency.write_text(
                    self.cases["changed_dependency"], encoding="utf-8", newline=""
                )
                changed = await client.call_tool("diagnostics", {"uri": self.source.as_uri()})
                self.assertFalse(changed.is_error, changed.content)
                self.assertNotEqual(
                    dependency_generation, changed.structured_content["workspace_generation"]
                )
                items = changed.structured_content["result"]["items"]
                self.assertEqual(len(items), 1)
                self.assertEqual(items[0]["code"], self.cases["expected"]["code"])
                self.assertEqual(items[0]["range"], self.cases["expected"]["dependency_range"])
