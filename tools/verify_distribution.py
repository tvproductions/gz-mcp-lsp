"""Verify built artifacts and installed CLI behavior outside the checkout."""

import json
import os
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*command: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run a verification command and retain decoded failure diagnostics."""
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="strict",
        capture_output=True,
        check=True,
    )


def verify_archives(wheel: Path, sdist: Path) -> None:
    """Allow only the owned update skill and verify every packaged resource."""
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        skill = "templates/skills/update-gz-template/SKILL.md"
        allowed = f"skills_first_starter/resources/{skill}"
        if {name for name in names if name.endswith("/SKILL.md")} != {allowed}:
            raise ValueError("Wheel must contain exactly the template-owned update skill")
        if any(name.startswith(("tests/", "tools/")) for name in names):
            raise ValueError("Unexpected development files or skills in wheel")
        for relative in (
            "bundle.json",
            ".agents/plugins/marketplace.json",
            ".claude-plugin/marketplace.json",
            "templates/AGENTS.skills-first.md",
            skill,
        ):
            content = archive.read(f"skills_first_starter/resources/{relative}")
            if content != (ROOT / relative).read_bytes():
                raise ValueError(f"Wheel resource differs from authority: {relative}")
    with tarfile.open(sdist) as archive:
        names = archive.getnames()
        if not any(name.endswith("/tests/test_starter.py") for name in names):
            raise ValueError("Source distribution is missing adoption tests")
        for relative in (
            ".github/dependabot.yml",
            "baselines/xplane/pyproject.toml",
            "baselines/xplane/uv.lock",
            "baselines/xplane/.python-version",
            "baselines/xplane/README.md",
            "tools/engineering/cognitive_qualification.py",
            "tools/engineering/cognitive_check.py",
            "tools/engineering/fixtures/cognitive-v1.json",
        ):
            if not any(name.endswith(f"/{relative}") for name in names):
                raise ValueError(f"Source distribution is missing baseline input: {relative}")
        if any("/.venv/" in name for name in names):
            raise ValueError("Source distribution contains a development environment")


def main() -> None:
    """Inspect archives and exercise the installed helper outside the checkout."""
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    version = metadata["project"]["version"]
    wheel = ROOT / "dist" / f"skills_first_starter-{version}-py3-none-any.whl"
    sdist = ROOT / "dist" / f"skills_first_starter-{version}.tar.gz"
    verify_archives(wheel, sdist)
    with tempfile.TemporaryDirectory(prefix="starter-wheel-") as temporary:
        directory = Path(temporary)
        environment = directory / "env"
        run("uv", "venv", "--python", sys.executable, str(environment), cwd=directory)
        scripts = environment / ("Scripts" if os.name == "nt" else "bin")
        python = scripts / ("python.exe" if os.name == "nt" else "python")
        command = scripts / (
            "skills-first-starter.exe" if os.name == "nt" else "skills-first-starter"
        )
        run(
            "uv",
            "pip",
            "install",
            "--offline",
            "--no-deps",
            "--python",
            str(python),
            str(wheel),
            cwd=directory,
        )
        run(str(command), "validate", cwd=directory)
        result = run(str(python), "-I", "-m", "skills_first_starter", "version", cwd=directory)
        if json.loads(result.stdout)["template_version"] != version:
            raise ValueError("Installed version differs from project metadata")
        target = directory / "adopter"
        target.mkdir()
        args = (str(command), "configure", "--project", str(target), "--starter-ref", "a" * 40)
        run(*args, cwd=directory)
        if list(target.iterdir()):
            raise ValueError("Installed preview wrote project files")
        run(*args, "--apply", cwd=directory)
        if (target / ".agents/skills/update-gz-template/SKILL.md").read_bytes() != (
            ROOT / "templates/skills/update-gz-template/SKILL.md"
        ).read_bytes():
            raise ValueError("Installed helper did not seed the canonical update skill")
        repeated = json.loads(run(*args, "--apply", cwd=directory).stdout)
        if repeated["writes"]:
            raise ValueError("Installed repeated adoption was not a no-op")
        status = json.loads(
            run(str(command), "status", "--project", str(target), cwd=directory).stdout
        )
        if status["runtime_readiness"] != "unverified":
            raise ValueError("Installed helper falsely claimed runtime readiness")
        refused = subprocess.run(
            [str(command), "configure", "--project", str(target)],
            cwd=directory,
            text=True,
            encoding="utf-8",
            errors="strict",
            capture_output=True,
            check=False,
        )
        if refused.returncode != 2:
            raise ValueError("Installed helper inferred provenance outside a starter checkout")
    print("Wheel resources, sdist contents and isolated installed CLI checks passed.")


if __name__ == "__main__":
    main()
