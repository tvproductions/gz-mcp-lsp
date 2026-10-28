"""On-demand public CLI tests for the Lizard counting contract."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def branches(count):
    return (
        "def f(x):\n"
        + "".join(f"    if x == {i}: return {i}\n" for i in range(count))
        + "    return -1\n"
    )


class CountingTests(unittest.TestCase):
    def run_check(self, sources, scopes=None, symlink=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, source in sources.items():
                (root / name).write_text(source, encoding="utf-8")
            if symlink:
                (root / "link.py").symlink_to(root / "a.py")
            output = root / "receipt.json"
            command = [
                sys.executable,
                str(Path(__file__).with_name("complexity_check.py")),
                "--root",
                str(root),
                "--paths",
                *(scopes or ["."]),
                "--output",
                str(output),
            ]
            run = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="strict",
                timeout=15,
            )
            self.assertTrue(output.exists(), run.stderr)
            return run.returncode, json.loads(output.read_text())

    def test_boundary_and_all_three_failures(self):
        code, report = self.run_check({"a.py": branches(19)})
        self.assertEqual((code, report["aggregate"]["maximum"]), (0, 20))
        code, report = self.run_check({"a.py": branches(20)})
        self.assertEqual(code, 1)
        self.assertEqual(
            {v["kind"] for v in report["violations"]}, {"function", "module", "overall"}
        )

    def test_weighted_average_and_scope_deduplication(self):
        code, report = self.run_check(
            {
                "a.py": branches(20) + "\ndef simple():\n    return 1\n",
                "b.py": "def simple():\n    return 1\n",
            },
            [".", "a.py"],
        )
        self.assertEqual(code, 1)
        self.assertEqual(report["aggregate"]["functions"], 3)
        self.assertAlmostEqual(report["aggregate"]["overall_mean"], 23 / 3)
        self.assertEqual([v["kind"] for v in report["violations"]], ["function"])

    def test_nested_methods_async_generics_and_assertions(self):
        source = "class C:\n    async def f[T](self, x:T):\n        def inner(y):\n            if y: return 1\n            return 0\n        assert x\n        assert x and self\n        if x: return inner(x)\n        return 0\n"
        code, report = self.run_check({"a.py": source})
        self.assertEqual(code, 0)
        functions = report["modules"][0]["functions"]
        self.assertEqual([(f["line"], f["complexity"]) for f in functions], [(3, 2), (2, 3)])

    def test_empty_module_and_script_are_not_function_scores(self):
        code, report = self.run_check({"a.py": "class Empty: pass\nx = lambda y: y\nif x: pass\n"})
        self.assertEqual(code, 0)
        self.assertIsNone(report["modules"][0]["mean"])
        self.assertIsNone(report["aggregate"]["overall_mean"])

    def test_parse_error_cannot_pass_partial_scope(self):
        code, report = self.run_check(
            {"a.py": "def broken(:\n", "b.py": "def f():\n    return 1\n"}
        )
        self.assertEqual((code, report["status"]), (2, "error"))
        self.assertEqual(len(report["errors"]), 1)

    def test_generated_directive_cannot_hide_function(self):
        code, report = self.run_check({"a.py": "# GENERATED CODE\n" + branches(20)})
        self.assertEqual(code, 2)
        self.assertIn("discovery mismatch", report["errors"][0]["message"])

    def test_missing_scope_and_symlink_fail_closed(self):
        code, _ = self.run_check({"a.py": "pass\n"}, ["missing"])
        self.assertEqual(code, 2)
        code, _ = self.run_check({"a.py": "pass\n"}, symlink=True)
        self.assertEqual(code, 2)
        code, report = self.run_check({"a.py": "pass\n"}, ["link.py"], symlink=True)
        self.assertEqual(code, 2)
        self.assertIn("Symlink scope", report["errors"][0]["message"])

    def test_escaping_absolute_and_excluded_scopes_fail_before_discovery(self):
        for scope, message in (
            ("../outside", "relative paths inside root"),
            (str(Path(__file__).resolve()), "relative paths inside root"),
            (".git", "Excluded scope"),
        ):
            with self.subTest(scope=scope):
                code, report = self.run_check({"a.py": "pass\n"}, [scope])
                self.assertEqual((code, report["status"]), (2, "error"))
                self.assertEqual(report["modules"], [])
                self.assertIn(message, report["errors"][0]["message"])

    def test_inline_suite_reports_unsupported_measurement(self):
        code, report = self.run_check({"a.py": "def café(x): assert x; return x\n"})
        self.assertEqual(code, 2)
        self.assertIn("discovery mismatch", report["errors"][0]["message"])

    def test_unicode_multiline_suite(self):
        code, report = self.run_check({"a.py": "def café(x):\n    assert x\n    return x\n"})
        self.assertEqual(code, 0)
        self.assertEqual(report["aggregate"]["maximum"], 1)

    def test_empty_scope_is_an_error(self):
        code, report = self.run_check({})
        self.assertEqual(code, 2)
        self.assertIn("no Python files", report["errors"][0]["message"])


if __name__ == "__main__":
    unittest.main()
