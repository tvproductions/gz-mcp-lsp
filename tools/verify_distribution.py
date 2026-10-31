"""Verify the design-stage distribution outside its source checkout."""

import json
import os
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import zipfile
from email import message_from_string
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*command: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run an artifact check with explicit arguments and failure propagation."""
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=True)


def verify_archives(wheel: Path, sdist: Path, version: str) -> None:
    """Reject wrong product identity, unintended dependencies and development leakage."""
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        if "gz_mcp_lsp/py.typed" not in names:
            raise ValueError("Wheel is missing the typing marker")
        if any(name.startswith(("skills_first_starter/", "tests/", "tools/")) for name in names):
            raise ValueError("Wheel includes starter runtime or development files")
        info = archive.read(f"gz_mcp_lsp-{version}.dist-info/METADATA").decode()
        metadata = message_from_string(info)
        dependencies = {value.replace(" ", "") for value in metadata.get_all("Requires-Dist", [])}
        if metadata["Name"] != "gz-mcp-lsp" or dependencies != {"mcp==2.3.0"}:
            raise ValueError("Unexpected distribution identity or dependencies")
    with tarfile.open(sdist) as archive:
        names = archive.getnames()
        if any("/.venv/" in name for name in names):
            raise ValueError("Source archive contains a development environment")
        if not any(name.endswith("/tests/README.md") for name in names):
            raise ValueError("Source archive lost the explicit product-test status")


def main() -> None:
    """Check metadata, archives and an isolated noneditable installed import."""
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    version = metadata["project"]["version"]
    wheel = ROOT / "dist" / f"gz_mcp_lsp-{version}-py3-none-any.whl"
    sdist = ROOT / "dist" / f"gz_mcp_lsp-{version}.tar.gz"
    verify_archives(wheel, sdist, version)
    with tempfile.TemporaryDirectory(prefix="gz-mcp-lsp-wheel-") as temporary:
        directory = Path(temporary)
        environment = directory / "env"
        run("uv", "venv", "--python", sys.executable, str(environment), cwd=directory)
        scripts = environment / ("Scripts" if os.name == "nt" else "bin")
        python = scripts / ("python.exe" if os.name == "nt" else "python")
        run("uv", "pip", "install", "--python", str(python), str(wheel), cwd=directory)
        result = run(
            str(python),
            "-I",
            "-c",
            "import gz_mcp_lsp, importlib.metadata, json; "
            "print(json.dumps({'origin': gz_mcp_lsp.__file__, "
            "'version': importlib.metadata.version('gz-mcp-lsp')}))",
            cwd=directory,
        )
        installed = json.loads(result.stdout)
        if installed["version"] != version:
            raise ValueError("Installed version differs from metadata")
        if not Path(installed["origin"]).is_relative_to(environment):
            raise ValueError("Import did not originate from the clean environment")
        executable = scripts / ("gz-mcp-lsp.exe" if os.name == "nt" else "gz-mcp-lsp")
        help_result = run(str(executable), "--help", cwd=directory)
        if "--config" not in help_result.stdout:
            raise ValueError("Installed entry point did not expose explicit configuration")
        invalid = subprocess.run(
            [str(executable), "--config", str(directory / "missing.json")],
            cwd=directory,
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        if invalid.returncode == 0 or invalid.stdout or "INVALID_INPUT" not in invalid.stderr:
            raise ValueError("Installed CLI did not reject missing settings cleanly")
    print("Wheel/sdist identity, installed import and CLI passed; semantic acceptance separate.")


if __name__ == "__main__":
    main()
