"""On-demand portability regression for the complexity compatibility probe."""

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from tools.engineering import evaluate_complexity


class ProbePortabilityTests(unittest.TestCase):
    def test_qualification_rejects_the_keyword_conditional_blind_spot(self):
        score = evaluate_complexity.code_complexity

        def broken_keywords(source):
            if source.startswith("def choose(x):") and "return dict(" in source:
                return SimpleNamespace(functions=[SimpleNamespace(name="choose", complexity=0)])
            return score(source)

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "qualification.json"
            with (
                mock.patch.object(evaluate_complexity, "code_complexity", broken_keywords),
                mock.patch.object(sys, "argv", ["evaluate_complexity", "--output", str(output)]),
                redirect_stdout(io.StringIO()),
            ):
                result = evaluate_complexity.main()
            self.assertEqual(result, 1)
            receipt = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(receipt["compatibility"], "failed")
            self.assertEqual(
                receipt["synthetic_cases"]["conditional_tuple"]["cognitive"]["choose"], 9
            )
            self.assertEqual(
                receipt["cognitive_canary_failures"],
                [{"case": "conditional_keywords", "expected": 9, "observed": 0}],
            )

    def test_source_encoding_is_independent_of_windows_legacy_locale(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "example.py"
            source.write_bytes("# coding: utf-8\n# “示例”\ndef sample():\n    return 1\n".encode())
            read_text = Path.read_text

            def legacy_read(path, *args, **kwargs):
                kwargs.setdefault("encoding", "cp1252")
                return read_text(path, *args, **kwargs)

            with mock.patch.object(Path, "read_text", autospec=True, side_effect=legacy_read):
                scores = evaluate_complexity.lizard_scores(source)
            self.assertEqual(scores, [{"name": "sample", "line": 3, "cyclomatic": 1}])


if __name__ == "__main__":
    unittest.main()
