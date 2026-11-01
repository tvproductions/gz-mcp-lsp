"""Direct ty and installed SDK/adapter navigation on independently expected symbols."""

import asyncio
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from mcp.client import Client
from mcp.client.stdio import StdioServerParameters

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.session import Session
from tests.integration.support import install_adapter


class ActualNavigationTests(unittest.IsolatedAsyncioTestCase):
    """No indexing sleeps or capability skips on a claimed platform."""

    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.outside = Path(cls.temporary.name).resolve()
        cls.checkout = Path(__file__).resolve().parents[2]
        cls.python, cls.ty = install_adapter(cls.checkout, cls.outside)

    async def asyncSetUp(self):
        self.root = self.outside / self._testMethodName
        shutil.copytree(self.checkout / "tests/fixtures/semantic_workspace", self.root)
        self.expected = json.loads(
            (self.root / "navigation_expected.json").read_text(encoding="utf-8")
        )
        self.uri = (self.root / self.expected["query"]["file"]).as_uri()
        self.position = self.expected["query"]["position"]
        self.arguments = {"uri": self.uri, "position": self.position}
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
        """Run the installed module with source checkout excluded from imports."""
        return Client(
            StdioServerParameters(
                command=str(self.python),
                args=["-I", "-m", "gz_mcp_lsp", "--config", str(self.settings)],
                cwd=str(self.outside),
            )
        )

    def sites(self, locations):
        """Keep source coordinate provenance independent from output presentation."""
        return sorted(
            (
                Path(item["uri"]).name,
                item["range"]["start"]["line"],
                item["range"]["start"]["character"],
            )
            for item in locations
        )

    async def test_exact_reference_sites_imports_and_definition_source(self):
        """Three expected call sites and imports agree with direct ty; decoy is absent."""
        direct = Session(Config(self.root, self.ty))
        raw = {}
        async with direct:
            await direct.rpc.notify(
                "textDocument/didOpen",
                {
                    "textDocument": {
                        "uri": self.uri,
                        "languageId": "python",
                        "version": 1,
                        "text": (self.root / self.expected["query"]["file"]).read_text(
                            encoding="utf-8"
                        ),
                    }
                },
            )
            for flag in (False, True):
                raw[flag] = await direct.rpc.request(
                    "textDocument/references",
                    {
                        "textDocument": {"uri": self.uri},
                        "position": self.position,
                        "context": {"includeDeclaration": flag},
                    },
                    timeout=20,
                )
        expected_call_sites = sorted(
            (item["file"], item["line"], item["character"]) for item in self.expected["calls"]
        )
        expected_imports = sorted(
            (item["file"], item["line"], item["character"]) for item in self.expected["imports"]
        )
        expected_without = expected_call_sites
        self.assertEqual(self.sites(raw[False]), expected_without)
        expected_with = sorted([*expected_without, *expected_imports, ("library.py", 5, 4)])
        self.assertEqual(self.sites(raw[True]), expected_with)
        async with asyncio.timeout(40):
            async with self.client() as client:
                for flag, expected_sites in ((False, expected_without), (True, expected_with)):
                    result = await client.call_tool(
                        "references",
                        {**self.arguments, "include_declaration": flag, "context_lines": 1},
                    )
                    self.assertFalse(result.is_error, result.content)
                    locations = result.structured_content["result"]["locations"]
                    self.assertEqual(self.sites(locations), self.sites(raw[flag]))
                    self.assertEqual(self.sites(locations), expected_sites)
                    observed_call_sites = [site for site in self.sites(locations) if site[1] == 2]
                    self.assertEqual(expected_call_sites, observed_call_sites)
                    reference_uris = [item["uri"] for item in locations]
                    decoy_uri = (self.root / self.expected["decoy"]).as_uri()
                    self.assertNotIn(decoy_uri, reference_uris)
                    self.assertTrue(all("context" in item for item in locations))
                definition = await client.call_tool("definition", self.arguments)
                self.assertFalse(definition.is_error, definition.content)
                targets = definition.structured_content["result"]["locations"]
                self.assertEqual(len(targets), 1)
                target = targets[0]
                self.assertEqual(target["uri"], (self.root / "library.py").as_uri())
                self.assertEqual(
                    target["selection_range"]["start"], self.expected["definition"]["identifier"]
                )
                self.assertEqual(target["source"]["text"], self.expected["definition"]["source"])
                self.assertEqual(
                    target["source"]["full_range"]["start"],
                    self.expected["definition"]["full_start"],
                )
                self.assertTrue(target["source"]["complete"])
                self.assertNotEqual(target["range"], target["selection_range"])

    async def test_class_nested_async_and_constant_complete_source(self):
        """Source is complete for supported class, nested decorated async and constant fixtures."""
        async with asyncio.timeout(40):
            async with self.client() as client:
                for case in self.expected["source_cases"]:
                    result = await client.call_tool(
                        "definition", {"uri": self.uri, "position": case["position"]}
                    )
                    self.assertFalse(result.is_error, result.content)
                    locations = result.structured_content["result"]["locations"]
                    self.assertEqual(len(locations), 1)
                    self.assertEqual(locations[0]["source"]["text"], case["expected_text"])
                    self.assertTrue(locations[0]["source"]["complete"])

    async def test_non_bmp_caller_coordinates(self):
        """Non-BMP prefix uses UTF-16 rather than Python/UTF-8 indexing."""
        arguments = {
            "uri": (self.root / "consumer_c.py").as_uri(),
            "position": {"line": 2, "character": 20},
        }
        async with self.client() as client:
            result = await client.call_tool("definition", arguments)
            self.assertFalse(result.is_error, result.content)
            self.assertEqual(
                result.structured_content["result"]["locations"][0]["selection_range"]["start"],
                self.expected["definition"]["identifier"],
            )
            invalid = await client.call_tool(
                "definition", {**arguments, "position": {"line": 2, "character": 14}}
            )
            self.assertTrue(invalid.is_error)
            self.assertEqual(invalid.structured_content["error"]["code"], "INVALID_INPUT")

    async def test_keyword_control_empty_hover_and_changed_dependency(self):
        """No identifier fallback, truthful no-match, and fresh source after an unopened edit."""
        async with asyncio.timeout(40):
            async with self.client() as client:
                control = await client.call_tool(
                    "definition",
                    {
                        "uri": (self.root / "library.py").as_uri(),
                        "position": self.expected["query"]["keyword_control"],
                    },
                )
                self.assertFalse(control.is_error, control.content)
                self.assertEqual(control.structured_content["result"]["locations"], [])
                empty = await client.call_tool(
                    "hover", {"uri": self.uri, "position": {"line": 1, "character": 0}}
                )
                self.assertFalse(empty.is_error, empty.content)
                self.assertIsNone(empty.structured_content["result"])
                before = await client.call_tool("definition", self.arguments)
                self.assertFalse(before.is_error, before.content)
                library = self.root / "library.py"
                library.write_bytes(
                    library.read_bytes().replace(b"return name.upper()", b"return name.lower()")
                )
                after = await client.call_tool("definition", self.arguments)
                self.assertFalse(after.is_error, after.content)
                self.assertNotEqual(
                    before.structured_content["workspace_generation"],
                    after.structured_content["workspace_generation"],
                )
                self.assertIn(
                    "return name.lower()",
                    after.structured_content["result"]["locations"][0]["source"]["text"],
                )
