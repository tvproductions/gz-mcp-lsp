"""Source parity without inferring future semantic query coordinates."""

import hashlib
import unittest
from typing import cast

from gz_mcp_lsp.models import FileIdentity, Position, Range, Snapshot
from gz_mcp_lsp.source_text import declaration


def snapshot(text):
    data = text.encode()
    return Snapshot(
        "file:///sample.py",
        data,
        hashlib.sha256(data).hexdigest(),
        1,
        FileIdentity(1, 2, 0o100644, 1),
    )


class SourceTests(unittest.TestCase):
    """Public invented declarations distinguish AST bytes from LSP code units."""

    def test_full_decorated_nested_async_source(self):
        source = snapshot(
            "def outer():\n    @wrapper(1)\n    async def inner(value: str):\n        return value\n    return inner\n"
        )
        result = declaration(source, Range(Position(2, 14), Position(2, 19)), None)
        self.assertEqual(
            result["source"],
            "    @wrapper(1)\n    async def inner(value: str):\n        return value",
        )
        self.assertEqual(result["source_status"], "complete")
        self.assertEqual(cast(dict, result["range"])["start"], {"line": 1, "character": 0})

    def test_ast_utf8_columns_differ_from_utf16(self):
        source = snapshot('value = "😀"; CONSTANT = 42\n')
        result = declaration(source, Range(Position(0, 14), Position(0, 22)), None)
        self.assertEqual(result["source"], "CONSTANT = 42")
        self.assertEqual(cast(dict, result["range"])["start"]["character"], 14)

    def test_incomplete_syntax_has_explicit_unavailable_source(self):
        result = declaration(
            snapshot("def broken(:\n"), Range(Position(0, 4), Position(0, 10)), None
        )
        self.assertEqual(result["source_status"], "unavailable")
