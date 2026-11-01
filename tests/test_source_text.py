"""Source extraction uses syntax/ranges, never semantic targeting guesses."""

import tempfile
import unittest
from pathlib import Path

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.models import Position, Range
from gz_mcp_lsp.workspace import Workspace


class SourceTextTests(unittest.TestCase):
    """Exact saved UTF-8 bytes, decorated/nested/async declarations and constants."""

    def setUp(self):
        try:
            from gz_mcp_lsp.source_text import declaration
        except ImportError as error:
            self.fail(f"Declaration extraction absent: {error}")
        self.declaration = declaration
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.source = self.root / "module.py"
        self.workspace = Workspace(Config(self.root, self.source))

    def extract(self, data, selection, symbols=None):
        self.source.write_bytes(data.encode("utf-8"))
        return self.declaration(self.workspace.read(self.source.as_uri()), selection, symbols)

    def test_full_decorated_nested_source(self):
        """The complete inner async function includes its decorator and multiline body."""
        text = (
            "class Outer:\n"
            "    @staticmethod\n"
            "    async def nested(\n"
            "        item: str,\n"
            "    ) -> str:\n"
            "        return item.upper()\n"
        )
        result = self.extract(text, Range(Position(2, 14), Position(2, 20)))
        self.assertEqual(result["text"], text[text.index("    @") :].rstrip("\n")[4:])
        self.assertEqual(result["source_status"], "complete")
        self.assertTrue(result["complete"])
        self.assertEqual(result["full_range"]["start"], {"line": 1, "character": 4})
        self.assertEqual(result["selection_range"]["start"], {"line": 2, "character": 14})

    def test_ast_utf8_columns_differ_from_utf16(self):
        """A non-ASCII prefix must not shift a constant's extracted source."""
        result = self.extract(
            'π = "😀"; CONSTANT = (\n    42\n)\n', Range(Position(0, 10), Position(0, 18))
        )
        self.assertEqual(result["text"], "CONSTANT = (\n    42\n)")
        self.assertEqual(result["full_range"]["start"], {"line": 0, "character": 10})

    def test_server_ranges_preserved_for_incomplete_syntax(self):
        """Known symbol bounds preserve text without claiming complete implementation."""
        symbols = [
            {
                "name": "broken",
                "kind": 12,
                "range": {"start": {"line": 0, "character": 0}, "end": {"line": 1, "character": 8}},
                "selectionRange": {
                    "start": {"line": 0, "character": 4},
                    "end": {"line": 0, "character": 10},
                },
            }
        ]
        result = self.extract(
            "def broken(:\n    pass\n", Range(Position(0, 4), Position(0, 10)), symbols
        )
        self.assertEqual(result["text"], "def broken(:\n    pass")
        self.assertEqual(result["source_status"], "syntax_incomplete")
        self.assertFalse(result["complete"])

    def test_incomplete_and_unmatched_source_are_explicit(self):
        """Never label a location fragment complete when declaration bounds are unknown."""
        result = self.extract("def broken(:\n", Range(Position(0, 4), Position(0, 10)))
        self.assertEqual(result["source_status"], "syntax_incomplete")
        self.assertFalse(result["complete"])
        result = self.extract("print('hello')\n", Range(Position(0, 0), Position(0, 5)))
        self.assertEqual(result["source_status"], "unavailable")
        self.assertFalse(result["complete"])
