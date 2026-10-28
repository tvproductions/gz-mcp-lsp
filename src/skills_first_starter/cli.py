#!/usr/bin/env python3
"""Preview or configure a project-scoped SP + SP-BP + gz-skills bundle.

No dependencies beyond Python 3.14. Native plugin managers own installation;
this tool writes project configuration and never edits their global caches.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

_SOURCE = Path(__file__).resolve()
_CHECKOUT = _SOURCE.parents[2]
# Editable installs use authoritative checkout files. Wheels carry checked copies.
HERE = (
    _CHECKOUT
    if _SOURCE.parent.parent.name == "src" and (_CHECKOUT / "bundle.json").is_file()
    else _SOURCE.parent / "resources"
)
MARKETPLACE = "skills-first-starter"
ORIGIN = "https://github.com/tvproductions/gz-skills-first-starter.git"
SHA = re.compile(r"[0-9a-f]{40}\Z")
UPDATE_SKILL = "update-gz-template"
UPDATE_SKILL_SOURCE = f"templates/skills/{UPDATE_SKILL}/SKILL.md"
UPDATE_SKILL_DESTINATION = f".agents/skills/{UPDATE_SKILL}/SKILL.md"


class AdoptionError(Exception):
    """Configuration requires reconciliation before adoption can proceed."""


def bundle() -> dict:
    """Read the authoritative bundle or its installed resource copy."""
    return json.loads((HERE / "bundle.json").read_text(encoding="utf-8"))


def template_version() -> str:
    """Read the starter-owned version independently of adopter app metadata."""
    version = bundle().get("template_version")
    if not isinstance(version, str) or not re.fullmatch(
        r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", version
    ):
        raise AdoptionError("template_version must be a numeric MAJOR.MINOR.PATCH version")
    return version


def validate_bundle() -> None:
    """Require matching immutable component pins in both native catalogs."""
    template_version()
    data = bundle()
    if data.get("schema_version") != 1:
        raise AdoptionError("unsupported bundle schema")
    parts = data.get("components", [])
    if {p["name"] for p in parts} != {"superpowers", "superpowers-backplane", "gz-skills"} or len(
        parts
    ) != 3:
        raise AdoptionError("bundle must contain exactly the three independently owned components")
    expected = {p["name"]: (p["repository"] + ".git", p["revision"]) for p in parts}
    if any(not SHA.fullmatch(p["revision"]) for p in parts):
        raise AdoptionError("every component needs an immutable full commit SHA")
    if any(type(p.get("enabled_by_default")) is not bool for p in parts):
        raise AdoptionError("every component needs an explicit boolean default activation")
    codex = json.loads((HERE / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    actual = {p["name"]: (p["source"]["url"], p["source"]["ref"]) for p in codex["plugins"]}
    if actual != expected or codex["name"] != MARKETPLACE:
        raise AdoptionError("Codex marketplace does not match bundle pins")
    claude = json.loads((HERE / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    # Claude Code reads "ref" as a branch or tag; a commit pin must use "sha".
    actual = {p["name"]: (p["source"]["url"], p["source"].get("sha")) for p in claude["plugins"]}
    if actual != expected or claude["name"] != MARKETPLACE:
        raise AdoptionError("Claude marketplace does not match bundle pins")


def check_path(root: Path, relative: str) -> Path:
    """Resolve a managed destination while rejecting symlinked parents."""
    path = root / relative
    for item in (path, *path.parents):
        if item == root:
            break
        if item.is_symlink():
            raise AdoptionError(f"refusing symlinked destination: {relative}")
        if item != path and item.exists() and not item.is_dir():
            raise AdoptionError(f"parent is not a directory: {relative}")
    if path.exists() and not path.is_file():
        raise AdoptionError(f"not a regular destination file: {relative}")
    return path


def profile_check(path: Path) -> None:
    """Preserve an existing explicit profile and reject incompatible state."""
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    if (
        not isinstance(data, dict)
        or set(data) != {"schema_version", "profile"}
        or type(data["schema_version"]) is not int
        or data["schema_version"] != 1
        or data["profile"] not in (None, "lite", "heavy")
    ):
        raise AdoptionError(
            "existing gz-skills profile is unsupported; reconcile it without overwriting"
        )


def _check_plugin_activation(plugins: dict, parts: list[dict]) -> None:
    """Reject conflicting activation and duplicate sources before adding tables."""
    defaults = {part["name"]: part["enabled_by_default"] for part in parts}
    for key, value in plugins.items():
        name = key.split("@")[0]
        if name not in defaults:
            continue
        if key.endswith("@" + MARKETPLACE):
            if value.get("enabled") is not defaults[name]:
                raise AdoptionError(
                    f"{key} conflicts with the default activation; reconcile explicitly"
                )
        elif value.get("enabled") is not False:
            raise AdoptionError(
                f"{key} may create duplicate discovery; adopt the existing source explicitly"
            )


def _missing_config_tables(data: dict, ref: str, parts: list[dict]) -> list[str]:
    """Render only absent managed tables; differing existing tables are conflicts."""
    wanted = [("marketplaces", MARKETPLACE, {"source_type": "git", "source": ORIGIN, "ref": ref})]
    wanted += [
        ("plugins", p["name"] + "@" + MARKETPLACE, {"enabled": p["enabled_by_default"]})
        for p in parts
    ]
    added = []
    for group, name, values in wanted:
        found = data.get(group, {}).get(name)
        if found is not None:
            if found != values:
                raise AdoptionError(f"conflicting [{group}.{name}] configuration; no files changed")
            continue
        lines = [f"[{group}.{json.dumps(name)}]"]
        lines += [f"{key} = " + json.dumps(value) for key, value in values.items()]
        added.append("\n".join(lines))
    return added


def project_config(existing: str, ref: str) -> str:
    """Extend compatible Codex configuration without replacing project settings."""
    data = tomllib.loads(existing)
    parts = bundle()["components"]
    _check_plugin_activation(data.get("plugins", {}), parts)
    added = _missing_config_tables(data, ref, parts)
    if not added:
        return existing
    return (
        existing
        + ("\n" if existing and not existing.endswith("\n") else "")
        + "\n"
        + "\n\n".join(added)
        + "\n"
    )


def _adoption_root(project: Path) -> Path:
    """Resolve the existing project and preserve the separate gzkit ecosystem."""
    root = project.resolve(strict=True)
    if not root.is_dir():
        raise AdoptionError("project must be an existing directory")
    if (root / ".gzkit").exists() or (root / ".gzkit").is_symlink():
        raise AdoptionError(
            "this is a gzkit project; keep that ecosystem and do not initialize this stack"
        )
    return root


def _check_discovery_entry(surface: str, child: Path) -> None:
    """Preserve legacy and shared skill copies for explicit reconciliation."""
    if child.name == UPDATE_SKILL and surface != ".agents/skills":
        raise AdoptionError(f"duplicate template update skill at {surface}; reconcile first")
    if child.name in ("skills-first-start", "adopt-skills-stack", "python-engineering"):
        raise AdoptionError(
            f"legacy starter skill at {surface}/{child.name}; "
            "reconcile with docs/migration-0.3.md before adoption; no files changed"
        )
    if child.name.startswith("gzs-") or child.name in (
        "superpowers",
        "superpowers-backplane",
        "managing-superpowers-backlog",
        "managing-superpowers-handoffs",
    ):
        raise AdoptionError(
            f"existing shared skill discovery at {surface}/{child.name}; reconcile first"
        )


def _check_discovery(root: Path) -> None:
    """Inspect all supported discovery surfaces without mutating their contents."""
    for surface in (".agents/skills", ".codex/skills", ".claude/skills", ".github/skills"):
        folder = root / surface
        if folder.is_symlink():
            raise AdoptionError(f"inspect existing discovery link {surface} before adoption")
        if folder.is_dir():
            for child in folder.iterdir():
                _check_discovery_entry(surface, child)


def _configuration_candidates(paths: dict[str, Path], ref: str) -> tuple[dict[str, str], dict]:
    """Prepare managed payloads without writing or changing existing authorities."""
    old_config = (
        paths[".codex/config.toml"].read_text(encoding="utf-8", newline="")
        if paths[".codex/config.toml"].exists()
        else ""
    )
    fragment = (HERE / "templates/AGENTS.skills-first.md").read_text(encoding="utf-8")
    lock = {
        "schema_version": 1,
        "starter": {"repository": ORIGIN, "version": template_version(), "revision": ref},
        "components": bundle()["components"],
    }
    candidates = {
        ".codex/config.toml": project_config(old_config, ref),
        ".skills-first/bundle.lock.json": json.dumps(lock, indent=2) + "\n",
        "AGENTS.skills-first.md": fragment,
        UPDATE_SKILL_DESTINATION: (HERE / UPDATE_SKILL_SOURCE).read_text(encoding="utf-8"),
    }
    if not paths["AGENTS.md"].exists():
        candidates["AGENTS.md"] = (
            "# Project agent instructions\n\nRead [AGENTS.skills-first.md](AGENTS.skills-first.md) for this project's development stack.\nAdd project-owned rules, verification commands, and operational skill routing here.\n"
        )
    return candidates, lock


def _plan_writes(
    paths: dict[str, Path], candidates: dict[str, str]
) -> tuple[dict[str, str], dict[str, bytes | None], list[str]]:
    """Check every candidate and capture rollback bytes before any write."""
    writes, before, present = {}, {}, []
    for name, payload in candidates.items():
        path = paths[name]
        current = path.read_bytes() if path.exists() else None
        before[name] = current
        if current == payload.encode():
            present.append(name)
        elif current is not None and name != ".codex/config.toml":
            raise AdoptionError(
                f"{name} differs from the reviewed template; reconcile without overwriting"
            )
        else:
            writes[name] = payload
    return writes, before, present


def _write_candidate(path: Path, payload: str, current: bytes | None) -> None:
    """Create exclusively or replace through a sibling temporary file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if current is None:
        with path.open("xb") as stream:
            stream.write(payload.encode())
        return
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temp = Path(stream.name)
        stream.write(payload.encode())
    try:
        os.chmod(temp, path.stat().st_mode & 0o777)
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def _apply_writes(
    root: Path,
    paths: dict[str, Path],
    writes: dict[str, str],
    before: dict[str, bytes | None],
) -> None:
    """Recheck each destination and roll completed writes back on failure."""
    completed = []
    try:
        for name, payload in writes.items():
            path = check_path(root, name)
            current = path.read_bytes() if path.exists() else None
            if current != before[name]:
                raise AdoptionError(f"{name} changed during preview; retry after review")
            _write_candidate(path, payload, current)
            completed.append(name)
    except BaseException:
        for name in reversed(completed):
            original = before[name]
            if original is None:
                paths[name].unlink()
            else:
                paths[name].write_bytes(original)
        raise


def configure(project: Path, ref: str, *, apply: bool = False) -> dict:
    """Preview or apply the reviewed adoption plan with conflict preservation."""
    validate_bundle()
    if not SHA.fullmatch(ref):
        raise AdoptionError(
            "use a reviewed, published full starter commit SHA; moving branches are not pins"
        )
    root = _adoption_root(project)
    _check_discovery(root)
    paths = {
        name: check_path(root, name)
        for name in (
            ".codex/config.toml",
            ".skills-first/bundle.lock.json",
            ".gz-skills/settings.json",
            "AGENTS.skills-first.md",
            "AGENTS.md",
            UPDATE_SKILL_DESTINATION,
        )
    }
    profile_check(paths[".gz-skills/settings.json"])
    candidates, lock = _configuration_candidates(paths, ref)
    writes, before, present = _plan_writes(paths, candidates)
    if apply:
        _apply_writes(root, paths, writes, before)
    return {
        "status": "configured" if apply else "preview",
        "project": str(root),
        "writes": list(writes),
        "present": present,
        "runtime_readiness": "unverified",
        "starter": lock["starter"],
        "next": [
            "Review the project instructions fragment; link it from existing AGENTS.md if needed.",
            "Profile selection belongs to canonical gz-skills setup; no profile is inferred or created.",
            "Follow docs/adoption.md for native installation and a fresh-session discovery check.",
            "Use the project update-gz-template skill for released template updates; verify discovery separately.",
        ],
    }


def status(project: Path) -> dict:
    """Compare managed project files with this starter's expected content."""
    root = project.resolve(strict=True)
    path = check_path(root, ".skills-first/bundle.lock.json")
    if not path.exists():
        return {"status": "not configured", "runtime_readiness": "unverified"}
    lock = json.loads(path.read_text(encoding="utf-8"))
    expected = configure(root, lock["starter"]["revision"])
    return {
        "status": "configured" if not expected["writes"] else "incomplete",
        "runtime_readiness": "unverified",
        "pending_files": expected["writes"],
        "starter": lock["starter"],
        "components": lock["components"],
    }


def backport(project: Path) -> dict:
    """Assess structure from names only; never read records or move files."""
    root = project.resolve(strict=True)
    if not root.is_dir():
        raise AdoptionError("project must be an existing directory")
    entries = []
    truncated = False
    with os.scandir(root) as items:
        for entry in items:
            if len(entries) >= 200:
                truncated = True
                break
            entries.append(
                {
                    "path": entry.name,
                    "kind": "symlink"
                    if entry.is_symlink()
                    else "directory"
                    if entry.is_dir(follow_symlinks=False)
                    else "file",
                }
            )
    names = {e["path"] for e in entries if e["kind"] != "symlink"}
    targets = [
        ("AGENTS.md", "Agent entry and links to project authorities"),
        ("docs/project/", "Purpose, architecture, and decisions when useful"),
        ("skills/", "Project-owned operational workflows; preserve native discovery"),
        (
            "src/<package>/ for Python",
            "Installed application/library code under the adopted Astral baseline; map existing sources and required refactors",
        ),
        (
            "existing data/evidence layout",
            "Keep inputs, records, and products separate from skills",
        ),
        (
            "existing planning authority",
            "Keep current backlog and handoff practice while SP-BP is deferred",
        ),
    ]
    return {
        "status": "assessment",
        "project": str(root),
        "writes": [],
        "inventory": sorted(entries, key=lambda e: e["path"]),
        "inventory_truncated": truncated,
        "preferred_structure": [{"target": t, "purpose": purpose} for t, purpose in targets],
        "existing_entrypoints": sorted(
            names & {"AGENTS.md", "README.md", "ROADMAP.md", "BACKLOG.md", "skills", "src", "docs"}
        ),
        "next": [
            "Read governing instructions; map existing sources to useful targets with authority and disposition recorded.",
            "Assess Python layout against the adopted Astral baseline; plan required refactors or evidence-backed exceptions while preserving public behavior and project authorities.",
            "Implement authorized changes in small verified steps; update imports, links, discovery, and verification commands for each move.",
        ],
        "backplane": "deferred",
        "assessment_limit": "Top-level names only; not a reviewed migration plan or code audit.",
    }


def source_revision() -> str:
    """Default only to this clean starter checkout, never a parent app's HEAD."""

    def git(*args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(HERE), *args],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
        ).stdout.strip()

    if Path(git("rev-parse", "--show-toplevel")).resolve() != HERE:
        raise AdoptionError("run from a standalone starter checkout or supply --starter-ref")
    origin = git("remote", "get-url", "origin")
    if origin not in (
        ORIGIN,
        ORIGIN.removesuffix(".git"),
        "git@github.com:tvproductions/skills-first-starter.git",
        "git@github.com:tvproductions/skills-first-starter",
        "https://github.com/tvproductions/skills-first-starter.git",
        "https://github.com/tvproductions/skills-first-starter",
        "git@github.com:tvproductions/gz-skills-first-starter.git",
        "git@github.com:tvproductions/gz-skills-first-starter",
    ):
        raise AdoptionError("this is an adopting repo; supply the published starter --starter-ref")
    if git("status", "--porcelain"):
        raise AdoptionError("starter checkout is dirty; use a reviewed clean revision")
    return git("rev-parse", "HEAD")


def main(argv: list[str] | None = None) -> int:
    """Dispatch the public CLI and render structured outcomes and failures."""
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    configure_parser = sub.add_parser(
        "configure", help="preview project configuration; --apply writes it"
    )
    configure_parser.add_argument("--project", type=Path, required=True)
    configure_parser.add_argument(
        "--starter-ref", help="full published starter SHA; defaults to this checkout HEAD"
    )
    configure_parser.add_argument("--apply", action="store_true")
    status_parser = sub.add_parser(
        "status", help="inspect configuration without claiming runtime installation"
    )
    status_parser.add_argument("--project", type=Path, required=True)
    backport_parser = sub.add_parser("backport", help="read-only preferred-structure assessment")
    backport_parser.add_argument("--project", type=Path, required=True)
    sub.add_parser("validate", help="validate the three bundle pins and both native catalogs")
    sub.add_parser("version", help="show this checkout's template version; not a release receipt")
    args = parser.parse_args(argv)
    try:
        if args.command == "configure":
            result = configure(
                args.project, args.starter_ref or source_revision(), apply=args.apply
            )
        elif args.command == "backport":
            result = backport(args.project)
        elif args.command == "status":
            result = status(args.project)
        elif args.command == "version":
            result = {"template_version": template_version()}
        else:
            validate_bundle()
            result = {
                "status": "valid",
                "template_version": template_version(),
                "components": bundle()["components"],
            }
        print(json.dumps(result, indent=2))
        return 0
    except (AdoptionError, OSError, ValueError, subprocess.SubprocessError, KeyError) as error:
        print(f"adoption blocked: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
