"""Test the qualification boundary, not a substitute scoring implementation."""

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from tools.engineering import cognitive_qualification as qualification


class QualificationTests(unittest.TestCase):
    """Use deliberately faulty adapters to prove the fixtures cannot silently pass."""

    def setUp(self):
        self.cases = json.loads(qualification.FIXTURES.read_bytes())["cases"]
        self.by_source = {case["source"]: case for case in self.cases}

    def fixture_adapter(self, source, filename):
        """Supply fixture answers solely to test report comparison and exit behavior."""
        case = self.by_source[source]
        if "error" in case:
            raise SyntaxError(filename)
        return [SimpleNamespace(**row) for row in case["scores"]]

    def test_fixture_syntax_and_locations_are_independently_validated(self):
        for case in self.cases:
            with self.subTest(case=case["name"]):
                if "error" in case:
                    with self.assertRaises(SyntaxError):
                        compile(case["source"], case["name"], "exec")
                else:
                    compile(case["source"], case["name"], "exec")
                    lines = case["source"].splitlines()
                    for row in case["scores"]:
                        self.assertIn("def ", lines[row["line"] - 1])
        self.assertEqual(len(self.by_source), len(self.cases))

    def test_fixture_adapter_only_proves_the_harness_comparison(self):
        report = qualification.qualify(self.fixture_adapter)
        self.assertEqual(report["status"], "passed")
        self.assertEqual(len(report["cases"]), 42)

    def test_known_keyword_blind_spot_is_a_failed_measurement(self):
        source = next(c["source"] for c in self.cases if c["name"] == "conditional_keywords")

        def faulty(candidate, filename):
            rows = self.fixture_adapter(candidate, filename)
            if candidate == source:
                rows[0].score = 0
            return rows

        report = qualification.qualify(faulty)
        failures = [row["case"] for row in report["cases"] if not row["passed"]]
        self.assertEqual(report["status"], "failed")
        self.assertEqual(failures, ["conditional_keywords"])

    def test_each_missing_discovery_context_fails_independently(self):
        for name in ("module_for", "module_while", "module_match", "method_under_class_match"):
            case = next(c for c in self.cases if c["name"] == name)
            with self.subTest(context=name):
                observed = qualification.observe(lambda _source, _filename: [], case)
                self.assertFalse(observed["passed"])

    def test_duplicate_function_names_must_retain_both_locations(self):
        case = next(c for c in self.cases if c["name"] == "guarded_duplicate_names")
        rows = self.fixture_adapter(case["source"], "fixture")
        self.assertFalse(qualification.observe(lambda _s, _f: rows[:1], case)["passed"])
        self.assertFalse(qualification.observe(lambda _s, _f: [rows[0], rows[0]], case)["passed"])

    def test_invalid_score_types_and_engine_errors_cannot_pass(self):
        case = self.cases[0]
        for score in (True, -1, "0", 0.0):
            with self.subTest(score=score):
                row = SimpleNamespace(name="plain", line=1, score=score)
                self.assertFalse(
                    qualification.observe(mock.Mock(return_value=[row]), case)["passed"]
                )
        observed = qualification.observe(mock.Mock(side_effect=RuntimeError("broken engine")), case)
        self.assertFalse(observed["passed"])
        self.assertEqual(observed["observed"]["error"], "RuntimeError")
        observed = qualification.observe(mock.Mock(side_effect=SystemExit(0)), case)
        self.assertFalse(observed["passed"])
        self.assertEqual(observed["observed"]["error"], "SystemExit")

    def test_invalid_source_requires_a_syntax_failure(self):
        for case in (case for case in self.cases if "error" in case):
            with self.subTest(case=case["name"]):
                self.assertFalse(qualification.observe(lambda _s, _f: [], case)["passed"])

    def test_missing_engine_cli_emits_error_and_exit_two(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "receipt.json"
            with (
                mock.patch.object(
                    sys,
                    "argv",
                    [
                        "qualification",
                        "--engine",
                        "missing_cognitive_engine:score",
                        "--output",
                        str(output),
                    ],
                ),
                redirect_stdout(io.StringIO()),
            ):
                result = qualification.main()
            self.assertEqual(result, 2)
            self.assertEqual(json.loads(output.read_text())["status"], "error")

    def test_an_unversioned_fixture_adapter_cannot_qualify_as_an_engine(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "receipt.json"
            module = SimpleNamespace(score=self.fixture_adapter)
            with (
                mock.patch.object(qualification.importlib, "import_module", return_value=module),
                mock.patch.object(qualification, "packages_distributions", return_value={}),
                mock.patch.object(
                    sys,
                    "argv",
                    ["qualification", "--engine", "fixture:score", "--output", str(output)],
                ),
                redirect_stdout(io.StringIO()),
            ):
                result = qualification.main()
            self.assertEqual(result, 2)
            self.assertIn("distribution metadata", json.loads(output.read_text())["error"])


if __name__ == "__main__":
    unittest.main()
