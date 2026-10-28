"""Verify the standalone X-Plane tool environment without simulator access."""

import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

BASELINE = Path(__file__).resolve().parents[1] / "baselines/xplane"


def run(directory: Path, *arguments: str, expected_exit: int = 0, diagnostic: str = "") -> None:
    """Require the expected command result, preserving diagnostics on failure."""
    result = subprocess.run(
        [sys.executable, "-m", *arguments],
        cwd=directory,
        text=True,
        encoding="utf-8",
        errors="strict",
        capture_output=True,
        check=False,
    )
    output = result.stdout + result.stderr
    if result.returncode != expected_exit or diagnostic not in output:
        raise RuntimeError(f"Unexpected result for {arguments}:\n{result.stdout}\n{result.stderr}")


def main() -> None:
    """Check exact runtime selection and functioning tools on invented inputs."""
    expected = (BASELINE / ".python-version").read_text(encoding="utf-8").strip()
    actual = ".".join(map(str, sys.version_info[:3]))
    if actual != expected:
        raise RuntimeError(f"Expected Python {expected}, got {actual}")
    if Path(sys.prefix).resolve() != (BASELINE / ".venv").resolve():
        raise RuntimeError("Run with the X-Plane project's exact synced environment")
    metadata = tomllib.loads((BASELINE / "pyproject.toml").read_text(encoding="utf-8"))
    if metadata["project"]["requires-python"] != ">=3.12,<3.13":
        raise RuntimeError("XPPython3 baseline must retain its reviewed Python family")
    with tempfile.TemporaryDirectory(prefix="xplane-tool-probe-") as temporary:
        directory = Path(temporary)
        (directory / "pyproject.toml").write_bytes((BASELINE / "pyproject.toml").read_bytes())
        sample = directory / "sample.py"
        sample.write_text("count: int = 1\n", encoding="utf-8")
        run(directory, "ruff", "check", "sample.py")
        run(directory, "ruff", "format", "--check", "sample.py")
        run(directory, "ty", "check", "sample.py")
        sample.write_text('count: int = "wrong"\n', encoding="utf-8")
        run(directory, "ty", "check", "sample.py", expected_exit=1, diagnostic="invalid-assignment")
        sample.write_text("print(undefined_name)\n", encoding="utf-8")
        run(directory, "ruff", "check", "sample.py", expected_exit=1, diagnostic="F821")
        test = directory / "test_probe.py"
        for expression, expected_exit in (("1 + 1, 2", 0), ("1 + 1, 3", 1)):
            test.write_text(
                "import unittest\n\n"
                "class Probe(unittest.TestCase):\n"
                f"    def test_arithmetic(self):\n        self.assertEqual({expression})\n",
                encoding="utf-8",
            )
            run(
                directory,
                "unittest",
                "discover",
                "-s",
                ".",
                "-v",
                expected_exit=expected_exit,
                diagnostic="Ran 1 test" if expected_exit == 0 else "FAILED (failures=1)",
            )
            # Avoid timestamp-granularity cache reuse between the two controls.
            for cached in (directory / "__pycache__").glob("test_probe.*.pyc"):
                cached.unlink()
        run(directory, "pre_commit", "--version")
        run(directory, "uv_build", "--help")
    print(f"Standalone X-Plane baseline checks passed on Python {actual}; host unverified.")


if __name__ == "__main__":
    main()
