"""Exercise consumer discovery/ceilings with fixture answers, never a private scorer."""

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from tools.engineering import cognitive_check as checker
from tools.engineering.cognitive_qualification import FIXTURES


class CognitiveGateTests(unittest.TestCase):
    """Prove the consumer refuses incomplete and invalid candidate measurements."""

    def setUp(self):
        self.cases = json.loads(FIXTURES.read_bytes())["cases"]
        self.by_source = {case["source"]: case for case in self.cases}
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()

    def fixture_adapter(self, source, filename):
        """Supply declared answers to isolate the consumer from scoring algorithms."""
        case = self.by_source[source]
        if "error" in case:
            raise SyntaxError(filename)
        return [SimpleNamespace(**row) for row in case["scores"]]

    def write_case(self, name, filename="sample.py"):
        case = next(case for case in self.cases if case["name"] == name)
        (self.root / filename).write_text(case["source"], encoding="utf-8")
        return case

    def test_ceiling_fifteen_passes_and_sixteen_fails(self):
        for score, status in ((15, "passed"), (16, "failed")):
            with self.subTest(score=score):
                self.write_case(f"ceiling_{score}")
                result = checker.assess(self.root, ["sample.py"], self.fixture_adapter)
                self.assertEqual(result["status"], status)
                self.assertEqual(result["aggregate"], {"functions": 1, "maximum": score})
                self.assertEqual(len(result["violations"]), int(score > 15))

    def test_inventory_uses_all_statement_containers_and_folds_nested_defs(self):
        for case in (case for case in self.cases if "scores" in case):
            with self.subTest(case=case["name"]):
                expected = [(row["name"], row["line"]) for row in case["scores"]]
                self.assertEqual(checker.inventory(case["source"], case["name"]), expected)

    def test_corpus_discovery_mismatch_fails_even_after_fixture_qualification(self):
        self.write_case("module_match")

        def incomplete(source, filename):
            return (
                self.fixture_adapter(source, filename)
                if filename.startswith("<qualification:")
                else []
            )

        result = checker.assess(self.root, ["sample.py"], incomplete)
        self.assertEqual(result["qualification"]["status"], "passed")
        self.assertEqual(result["status"], "error")
        self.assertIn("discovery mismatch", result["errors"][0]["message"])

    def test_valid_module_without_functions_has_no_synthetic_zero_score(self):
        self.write_case("function_free_module")
        result = checker.assess(self.root, ["sample.py"], self.fixture_adapter)
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["aggregate"], {"functions": 0, "maximum": None})

    def test_partial_scope_and_invalid_source_never_pass(self):
        self.write_case("plain")
        for paths in (["sample.py", "missing.py"], ["../escape.py"], [".venv"], []):
            with self.subTest(paths=paths):
                self.assertEqual(
                    checker.assess(self.root, paths, self.fixture_adapter)["status"], "error"
                )
        self.write_case("invalid_module_return")
        result = checker.assess(self.root, ["sample.py"], self.fixture_adapter)
        self.assertEqual(result["status"], "error")

    def test_failed_qualification_stops_corpus_measurement(self):
        self.write_case("plain")
        result = checker.assess(self.root, ["sample.py"], lambda _source, _filename: [])
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["modules"], [])

    def test_cli_missing_engine_is_an_error_not_an_empty_success(self):
        output = self.root / "receipt.json"
        with (
            mock.patch.object(
                sys,
                "argv",
                [
                    "cognitive_check",
                    "--engine",
                    "missing_cognitive_engine:score",
                    "--root",
                    str(self.root),
                    "--paths",
                    "sample.py",
                    "--output",
                    str(output),
                ],
            ),
            redirect_stdout(io.StringIO()),
        ):
            self.assertEqual(checker.main(), 2)
        self.assertEqual(json.loads(output.read_text())["status"], "error")


if __name__ == "__main__":
    unittest.main()
