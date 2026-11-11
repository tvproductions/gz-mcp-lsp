"""Exact public result budgets include Unicode bytes and reject non-JSON values."""

import math
import unittest

from gz_mcp_lsp.models import AdapterError
from gz_mcp_lsp.results import bounded, encoded_size


class ResultBudgetTests(unittest.TestCase):
    """Budget equality is permitted; an oversized result cannot be published."""

    def test_utf8_bytes_are_counted_without_ascii_escaping(self):
        """A JSON string includes its quotes and the actual UTF-8 payload bytes."""
        self.assertEqual(encoded_size("é😀"), 8)

    def test_nonfinite_numbers_are_not_json_results(self):
        """NaN and infinities fail serialization instead of escaping the byte contract."""
        for value in (math.nan, math.inf, -math.inf):
            with self.subTest(value=value), self.assertRaises(ValueError):
                encoded_size({"value": value})

    def test_budget_is_inclusive_and_oversize_is_result_limit(self):
        """Exactly the authorized size passes; one excess byte fails visibly."""
        value = "x" * 300
        self.assertEqual(bounded(value, 302), 302)
        with self.assertRaises(AdapterError) as raised:
            bounded(value, 301)
        self.assertEqual(raised.exception.code, "RESULT_LIMIT")
