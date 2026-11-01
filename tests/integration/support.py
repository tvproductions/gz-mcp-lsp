"""Prepare a locked installed adapter before integration calls."""

import os
import subprocess
import sys
from pathlib import Path


def install_adapter(checkout: Path, outside: Path) -> tuple[Path, Path]:
    """Install the wheel and exact runtime graph outside the source checkout."""

    ty = Path(sys.executable).parent / ("ty.exe" if os.name == "nt" else "ty")
    if not ty.is_file():
        raise AssertionError("Required pinned ty executable is missing")
    prefix = outside / "installed"
    python = prefix / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    commands = [
        ["uv", "build", "--no-sources", "--wheel", "--out-dir", str(outside / "dist")],
        ["uv", "venv", "--python", sys.executable, str(prefix)],
        [
            "uv",
            "export",
            "--locked",
            "--no-dev",
            "--no-emit-project",
            "--format",
            "pylock.toml",
            "--output-file",
            str(outside / "pylock.toml"),
        ],
        ["uv", "pip", "sync", "--offline", "--python", str(python), str(outside / "pylock.toml")],
    ]
    for command in commands:
        _run(command, checkout)
    wheel = next((outside / "dist").glob("*.whl"))
    _run(
        ["uv", "pip", "install", "--offline", "--no-deps", "--python", str(python), str(wheel)],
        outside,
    )
    return python, ty


def _run(command: list[str], cwd: Path) -> None:
    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode:
        raise AssertionError(result.stderr)
