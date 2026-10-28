"""On-demand Cosmic Ray compatibility proof using disposable unittest fixtures."""

import argparse
import hashlib
import json
import os
import platform
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from datetime import date
from importlib.metadata import version
from pathlib import Path

SOURCE = """def checked() -> int:
    return 1234


def unchecked() -> int:
    return 4321
"""
TESTS = """import unittest
import specimen


class SpecimenTests(unittest.TestCase):
    def test_checked(self):
        self.assertEqual(specimen.checked(), 1234)
"""
FAILING_TESTS = TESTS.replace("1234)", "0)")


def require(condition, message):
    """Keep proof checks active even when Python optimization is enabled."""
    if not condition:
        raise ValueError(message)


def classify(result):
    """Distinguish timeouts and broken workers from genuine test kills."""
    if result is None:
        return "pending"
    if result["worker_outcome"] != "normal" or result["test_outcome"] == "incompetent":
        return "tool_error"
    if result["output"] == "timeout":
        return "timeout"
    if result["test_outcome"] in ("killed", "survived"):
        return result["test_outcome"]
    return "tool_error"


def evaluate(directory):
    """Exercise CLI, controls, mutation results and source restoration in isolation."""
    cosmic = shutil.which("cosmic-ray")
    reporter = shutil.which("cr-report")
    require(cosmic and reporter, "Run with the selected Cosmic Ray environment.")
    deadline = time.monotonic() + 120
    commands = []

    def run(*command, expected=0):
        remaining = deadline - time.monotonic()
        require(remaining > 0, "Proof exceeded its 120-second budget.")
        result = subprocess.run(
            command,
            cwd=directory,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUTF8": "1"},
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            timeout=min(30, remaining),
            check=False,
        )
        commands.append({"argv": list(command), "exit": result.returncode})
        require(
            result.returncode == expected,
            f"Unexpected exit {result.returncode}: {command}\n{result.stdout}\n{result.stderr}",
        )
        return result.stdout

    def config(name, test_command, timeout=5.0):
        path = f"{name}.toml"
        (directory / path).write_text(
            '[cosmic-ray]\nmodule-path = "specimen.py"\nexcluded-modules = []\n'
            f"timeout = {timeout}\ntest-command = {json.dumps(test_command)}\n"
            '[cosmic-ray.distributor]\nname = "local"\n',
            encoding="utf-8",
        )
        return path

    def dump(session):
        return [json.loads(line) for line in run(cosmic, "dump", session).splitlines()]

    python = Path(sys.executable).as_posix()
    test_command = shlex.join([python, "-B", "-m", "unittest", "test_specimen", "-v"])
    (directory / "specimen.py").write_text(SOURCE, encoding="utf-8")
    source_bytes = (directory / "specimen.py").read_bytes()
    (directory / "test_specimen.py").write_text(TESTS, encoding="utf-8")
    (directory / "test_failing.py").write_text(FAILING_TESTS, encoding="utf-8")
    run(python, "-B", "-m", "unittest", "test_specimen", "-v")
    good_config = config("good", test_command)
    controls = {}
    cases = (
        ("passing", good_config, 0, "survived"),
        (
            "failing",
            config("failing", test_command.replace("test_specimen", "test_failing")),
            1,
            "killed",
        ),
        (
            "timeout",
            config(
                "timeout", shlex.join([python, "-c", "import time; time.sleep(2)"]), timeout=0.1
            ),
            1,
            "timeout",
        ),
        ("launch_error", config("launch_error", "./missing-proof-executable"), 0, "tool_error"),
    )
    for name, configuration, exit_code, expected_outcome in cases:
        session = f"{name}.sqlite"
        run(cosmic, "baseline", configuration, "--session-file", session, expected=exit_code)
        items = dump(session)
        require(len(items) == 1, f"Missing baseline result: {name}")
        outcome = classify(items[0][1])
        require(outcome == expected_outcome, f"Unexpected baseline outcome: {name}: {outcome}")
        controls[name] = {
            "cli_exit": exit_code,
            "classification": outcome,
            "worker_outcome": items[0][1]["worker_outcome"],
            "test_outcome": items[0][1]["test_outcome"],
        }

    # Mutation execution is permitted only after the genuine passing control.
    run(cosmic, "init", good_config, "mutations.sqlite")
    run(cosmic, "exec", good_config, "mutations.sqlite")
    items = dump("mutations.sqlite")
    counts = Counter(classify(result) for _, result in items)
    require(
        counts["killed"] > 0 and counts["survived"] > 0, "No meaningful kill/survival contrast."
    )
    require(set(counts) == {"killed", "survived"}, f"Broken mutation execution: {counts}")
    require(
        (directory / "specimen.py").read_bytes() == source_bytes,
        "Mutation execution did not restore the original source.",
    )
    run(python, "-B", "-m", "unittest", "test_specimen", "-v")
    report = run(reporter, "mutations.sqlite", "--show-diff", "--show-output")
    return {
        "commands": commands,
        "controls": controls,
        "counts": dict(counts),
        "mutations": items,
        "report": report,
        "source_restored": True,
    }


def main():
    """Write a new explicit receipt; do not overwrite existing evidence."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), "Choose an unused receipt path.")
    root = Path(__file__).resolve().parents[2]
    expected = (root / ".python-version").read_text(encoding="utf-8").strip()
    require(platform.python_version() == expected, f"Use the pinned Python {expected}.")
    with tempfile.TemporaryDirectory(prefix="starter-cosmic-proof-") as temporary:
        observation = evaluate(Path(temporary))
        serialized = json.dumps(observation)
        for original, replacement in (
            (temporary, "<disposable>"),
            (sys.prefix, "<environment>"),
            (Path(sys.prefix).as_posix(), "<environment>"),
        ):
            serialized = serialized.replace(json.dumps(original)[1:-1], replacement)
        observation = json.loads(serialized)
    receipt = {
        "date": date.today().isoformat(),
        "python": platform.python_version(),
        "platform": platform.system(),
        "cosmic_ray": version("cosmic-ray"),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "fixtures": {
            "specimen.py": SOURCE,
            "test_specimen.py": TESTS,
            "test_failing.py": FAILING_TESTS,
        },
        "budget_seconds": 120,
        "test_timeout_seconds": 5,
        "observations": observation,
    }
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, indent=2)
        stream.write("\n")
    print(
        json.dumps(
            {
                "compatibility": "passed",
                "python": receipt["python"],
                "cosmic_ray": receipt["cosmic_ray"],
                "counts": observation["counts"],
            }
        )
    )


if __name__ == "__main__":
    main()
