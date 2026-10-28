"""Explicit compatibility probe for the starter's on-demand complexity tools."""

import argparse
import hashlib
import json
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import tokenize
from datetime import date
from importlib.metadata import version
from pathlib import Path
from typing import TypedDict

import lizard
from complexipy import code_complexity, file_complexity


class FunctionScore(TypedDict):
    """Retain source identity and the two independent complexity measurements."""

    name: str
    line: int
    cognitive: int
    cyclomatic: int | None


def executable(name: str) -> str:
    """Locate a required analyzer in the selected environment."""
    path = shutil.which(name)
    if path is None:
        raise FileNotFoundError(f"Required analyzer is not installed: {name}")
    return path


def nested(depth):
    """Generate a nested conditional fixture with a controlled depth."""
    lines = ["def nested(value):"]
    for i in range(depth):
        lines.append("    " * (i + 1) + f"if value > {i}:")
    lines.append("    " * (depth + 1) + "return value")
    lines.append("    return 0")
    return "\n".join(lines) + "\n"


def flat(count):
    """Generate independent branches for the cyclomatic boundary probe."""
    return (
        "def flat(value):\n"
        + "".join(f"    if value == {i}:\n        return {i}\n" for i in range(count))
        + "    return -1\n"
    )


modern = """type Pair[T] = tuple[T, T]
def choose[T](values: list[T], fallback: T) -> T:
    if values:
        return values[0]
    return fallback

def describe(value: int):
    return t"Value: {value}"

def classify(value: int) -> int:
    match value:
        case 1:
            return 1
        case 2:
            return 2
        case 3:
            return 3
        case _:
            return 0
"""


def ruff_check(path, limit):
    command = [
        executable("ruff"),
        "check",
        "--isolated",
        "--target-version",
        "py314",
        "--select",
        "C901",
        "--config",
        f"lint.mccabe.max-complexity={limit}",
        "--output-format",
        "json",
        str(path),
    ]
    run = subprocess.run(
        command, capture_output=True, text=True, encoding="utf-8", errors="strict", timeout=30
    )
    assert run.returncode in (0, 1), run.stderr
    return run.returncode, json.loads(run.stdout)


def lizard_scores(path):
    """Measure compiled source through Lizard's public Python API."""
    with tokenize.open(path) as source:
        compile(source.read(), str(path), "exec")
    analysis = lizard.analyze_file(str(path))
    return [
        {"name": item.name, "line": item.start_line, "cyclomatic": item.cyclomatic_complexity}
        for item in analysis.function_list
    ]


def observe_case(name, code, directory):
    """Compare independent branching and nesting measures for valid Python."""
    compile(code, f"{name}.py", "exec")
    path = directory / f"{name}.py"
    path.write_text(code, encoding="utf-8")
    _, diagnostics = ruff_check(path, 0)
    cyclomatic = {
        diagnostic["message"].split("`")[1]: diagnostic_score(diagnostic)
        for diagnostic in diagnostics
    }
    ruff_exit, _ = ruff_check(path, 20)
    run = subprocess.run(
        [
            executable("complexipy"),
            str(path),
            "--max-complexity-allowed",
            "15",
            "--snapshot-ignore",
            "--no-ignore",
            "--cache-dir",
            str(directory / "cache"),
            "--plain",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        timeout=30,
    )
    assert run.returncode in (0, 1), (run.stdout, run.stderr)
    return {
        "cognitive": {
            function.name: function.complexity for function in code_complexity(code).functions
        },
        "cyclomatic": cyclomatic,
        "lizard": lizard_scores(path),
        "ruff_exit": ruff_exit,
        "complexipy_exit": run.returncode,
    }


def diagnostic_score(diagnostic):
    """Extract the measured score from pinned Ruff's C901 diagnostic."""
    match = re.search(r"\((\d+) >", diagnostic["message"])
    if match is None:
        raise ValueError(f"Unrecognized C901 diagnostic: {diagnostic['message']}")
    return int(match.group(1))


def verify_cases(observations, directory):
    """Require threshold behavior, modern syntax discovery and parse failure."""
    assert observations["flat_boundary"]["ruff_exit"] == 0, observations
    assert observations["flat_exceeds"]["ruff_exit"] == 1, observations
    assert observations["nested_boundary"]["cognitive"]["nested"] == 15, observations
    assert observations["nested_exceeds"]["cognitive"]["nested"] == 21, observations
    assert observations["nested_boundary"]["complexipy_exit"] == 0, observations
    assert observations["nested_exceeds"]["complexipy_exit"] == 1, observations
    assert observations["nested_exceeds"]["ruff_exit"] == 0, observations
    assert set(observations["modern"]["cognitive"]) == {"choose", "describe", "classify"}
    for name, expected in (("flat_boundary", 20), ("flat_exceeds", 21)):
        assert observations[name]["lizard"][0]["cyclomatic"] == expected, observations
    assert {item["name"] for item in observations["modern"]["lizard"]} == {
        "choose",
        "describe",
        "classify",
    }, observations
    invalid = directory / "invalid.py"
    invalid.write_text("def broken(:\n", encoding="utf-8")
    run = subprocess.run(
        [
            executable("complexipy"),
            str(invalid),
            "--cache-dir",
            str(directory / "cache"),
            "--plain",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        timeout=30,
    )
    assert run.returncode != 0, (run.stdout, run.stderr)


def inspect_source(root, relative):
    """Record actual source scores without suppressing existing violations."""
    path = root / relative
    result = file_complexity(str(path), no_ignore=True, check_script=True)
    _, diagnostics = ruff_check(path, 0)
    cyclomatic = {item["location"]["row"]: diagnostic_score(item) for item in diagnostics}
    functions: list[FunctionScore] = [
        {
            "name": function.name,
            "line": function.line_start,
            "cognitive": function.complexity,
            "cyclomatic": cyclomatic.get(function.line_start),
        }
        for function in result.functions
    ]
    measured = lizard_scores(path)
    return {
        "lizard": measured,
        "lizard_module_mean": (
            sum(item["cyclomatic"] for item in measured) / len(measured) if measured else None
        ),
        "file": relative,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "functions": functions,
        "ruff_over_20": [item["message"] for item in ruff_check(path, 20)[1]],
        "complexipy_over_15": [function for function in functions if function["cognitive"] > 15],
    }


def evaluate(root):
    """Return compatibility evidence separately from the code's policy failures."""
    cases = {
        "modern": modern,
        "flat_boundary": flat(19),
        "flat_exceeds": flat(20),
        "nested_boundary": nested(5),
        "nested_exceeds": nested(6),
        "conditional_tuple": (
            "def choose(x):\n    return ("
            + ", ".join(f"{i} if x[{i}] else 0" for i in range(9))
            + ")\n"
        ),
        "conditional_keywords": (
            "def choose(x):\n    return dict("
            + ", ".join(f"k{i}={i} if x[{i}] else 0" for i in range(9))
            + ")\n"
        ),
    }
    with tempfile.TemporaryDirectory(prefix="starter-complexity-") as temporary:
        directory = Path(temporary)
        observations = {name: observe_case(name, code, directory) for name, code in cases.items()}
        verify_cases(observations, directory)
    failures = [
        {"case": name, "expected": 9, "observed": observations[name]["cognitive"].get("choose")}
        for name in ("conditional_tuple", "conditional_keywords")
        if observations[name]["cognitive"].get("choose") != 9
    ]
    return {
        "compatibility": "failed" if failures else "passed",
        "cognitive_canary_failures": failures,
        "qualification_fixtures": {
            name: cases[name] for name in ("conditional_tuple", "conditional_keywords")
        },
        "date": date.today().isoformat(),
        "python": platform.python_version(),
        "versions": {
            "ruff": version("ruff"),
            "complexipy": version("complexipy"),
            "lizard": version("lizard"),
        },
        "thresholds": {"cyclomatic": 20, "cognitive": 15},
        "synthetic_cases": observations,
        "invalid_syntax_rejected": True,
        "source": [
            inspect_source(root, path)
            for path in (
                "tools/verify_distribution.py",
                "tools/engineering/test_evaluate_complexity.py",
                "tools/engineering/evaluate_complexity.py",
            )
        ],
        "limitations": [
            "Focused syntax and threshold checks, not complete Python grammar proof.",
            "Exploratory Lizard observations; use complexity_check.py for authoritative lizard-functions-v1 enforcement.",
            "Source violations remain visible; no refactoring or automatic baseline suppression.",
        ],
    }


def main():
    """Write one requested receipt; never change source or the saved baseline."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assert shutil.which("ruff") and shutil.which("complexipy"), "Use the hygiene group."
    receipt = evaluate(Path(__file__).resolve().parents[2])
    scores = [item["cyclomatic"] for source in receipt["source"] for item in source["lizard"]]
    receipt["lizard_aggregate"] = {
        "population": "reported functions across the explicit source scope",
        "functions": len(scores),
        "maximum": max(scores) if scores else None,
        "overall_function_weighted_mean": sum(scores) / len(scores) if scores else None,
        "enforcement": "observational; authoritative gate is complexity_check.py (lizard-functions-v1)",
    }
    args.output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "compatibility": receipt["compatibility"],
                "cognitive_canary_failures": receipt["cognitive_canary_failures"],
                "python": receipt["python"],
                "versions": receipt["versions"],
                "violating_sources": [
                    source["file"]
                    for source in receipt["source"]
                    if source["ruff_over_20"] or source["complexipy_over_15"]
                ],
            }
        )
    )
    return 1 if receipt["compatibility"] == "failed" else 0


if __name__ == "__main__":
    sys.exit(main())
