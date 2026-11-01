"""Load project-owned JSON settings; no application environment overrides."""

import json
import math
import platform
import sys
from dataclasses import dataclass, fields
from pathlib import Path
from typing import cast

from gz_mcp_lsp.models import AdapterError


@dataclass(frozen=True, slots=True)
class Limits:
    """Operator-configurable positive resource ceilings."""

    header_bytes: int = 4096
    frame_bytes: int = 16 * 1024 * 1024
    file_bytes: int = 2 * 1024 * 1024
    workspace_bytes: int = 64 * 1024 * 1024
    workspace_files: int = 10_000
    result_bytes: int = 1024 * 1024
    in_flight_reads: int = 8
    mutation_files: int = 100
    mutation_edits: int = 1000
    staged_bytes: int = 8 * 1024 * 1024
    retained_state_bytes: int = 256 * 1024 * 1024
    retained_plans: int = 32
    plan_ttl_seconds: int = 600


@dataclass(frozen=True, slots=True)
class Config:
    """Immutable authority, scope and budgets selected at startup."""

    workspace_root: Path
    ty_executable: Path
    state_directory: Path | None = None
    writable_roots: tuple[Path, ...] = ()
    mutations_enabled: bool = False
    request_timeout_seconds: float = 20
    initialize_timeout_seconds: float = 20
    shutdown_timeout_seconds: float = 3
    kill_timeout_seconds: float = 2
    limits: Limits = Limits()
    exclusions: tuple[str, ...] = ()
    project_config_files: tuple[str, ...] = ("pyproject.toml", "ty.toml")


def _mapping(value: object, allowed: set[str]) -> dict[str, object]:
    if not isinstance(value, dict) or any(key not in allowed for key in value):
        raise AdapterError("INVALID_INPUT", "Settings contain an unknown key or invalid object")
    return cast("dict[str, object]", value)


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise AdapterError("INVALID_INPUT", "Duplicate JSON setting")
        result[key] = value
    return result


def _reject_constant(value: str) -> object:
    raise AdapterError("INVALID_INPUT", "Nonfinite JSON number")


def _absolute(value: object) -> Path:
    if not isinstance(value, str) or "\0" in value:
        raise AdapterError("INVALID_INPUT", "Settings path must be an absolute local path")
    path = Path(value)
    if not path.is_absolute() or str(path).startswith(("\\\\", "//")):
        raise AdapterError("INVALID_INPUT", "Settings path must be an absolute local path")
    return path


def _relative_paths(value: object) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise AdapterError("INVALID_INPUT", "Scope paths must be a list")
    result = []
    for item in value:
        if not isinstance(item, str) or not item or any(c in item for c in "\0\\*?[]"):
            raise AdapterError("INVALID_INPUT", "Scope paths must be literal relative paths")
        path = Path(item)
        if path.is_absolute() or ".." in path.parts or item == ".":
            raise AdapterError("INVALID_INPUT", "Scope path escapes the workspace")
        result.append(path.as_posix())
    return tuple(result)


def _timeout(value: object) -> float:
    if type(value) not in (int, float):
        raise AdapterError("INVALID_INPUT", "Timeout requires a positive finite number")
    number = float(cast("float", value))
    if not math.isfinite(number) or number <= 0:
        raise AdapterError("INVALID_INPUT", "Timeout requires a positive finite number")
    return number


def _limits(value: object) -> Limits:
    raw = _mapping(value, {field.name for field in fields(Limits)})
    values: dict[str, int] = {}
    for key, number in raw.items():
        if type(number) is not int or number <= 0:
            raise AdapterError("INVALID_INPUT", "Resource limits require positive integers")
        values[key] = number
    return Limits(**values)


def write_platform_supported() -> bool:
    """A platform claim is necessary but not sufficient for the T8 filesystem proof."""
    machine = platform.machine().lower()
    return (sys.platform == "linux" and machine in {"x86_64", "amd64"}) or (
        sys.platform == "darwin" and machine in {"arm64", "aarch64"}
    )


def _authority(
    raw: object, state: object, root: Path
) -> tuple[bool, tuple[Path, ...], Path | None]:
    settings = _mapping(raw, {"enabled", "writable_roots"})
    enabled = settings.get("enabled", False)
    if type(enabled) is not bool:
        raise AdapterError("INVALID_INPUT", "Mutation enablement must be a boolean")
    raw_roots = settings.get("writable_roots", [])
    if not isinstance(raw_roots, list):
        raise AdapterError("INVALID_INPUT", "Writable roots must be a list")
    roots = tuple(_absolute(item).resolve(strict=True) for item in raw_roots)
    if any(not item.is_dir() or not item.is_relative_to(root) for item in roots):
        raise AdapterError("OUTSIDE_WORKSPACE", "Writable root is not a workspace directory")
    directory = _absolute(state).resolve() if state is not None else None
    if directory is not None and directory.exists() and not directory.is_dir():
        raise AdapterError("INVALID_INPUT", "Recovery state path is not a directory")
    if directory is not None and directory.is_relative_to(root):
        raise AdapterError("INVALID_INPUT", "Recovery state must be outside workspace source")
    if enabled and (not roots or directory is None):
        raise AdapterError("INVALID_INPUT", "Enabled mutations require explicit roots and state")
    if enabled and not write_platform_supported():
        raise AdapterError("UNSUPPORTED", "Writes are disabled on this platform")
    return enabled, roots, directory


def load_config(path: Path) -> Config:
    """Validate the complete JSON document without creating files or processes."""
    allowed = {
        "schema_version",
        "workspace_root",
        "ty_executable",
        "state_directory",
        "mutations",
        "request_timeout_seconds",
        "initialize_timeout_seconds",
        "shutdown_timeout_seconds",
        "kill_timeout_seconds",
        "limits",
        "exclusions",
        "project_config_files",
    }
    try:
        if path.stat().st_size > 65536:
            raise AdapterError("LIMIT_EXCEEDED", "Settings document exceeds 64 KiB")
        raw = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
        data = _mapping(raw, allowed)
        if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
            raise AdapterError("INVALID_INPUT", "Unsupported settings schema version")
        root = _absolute(data.get("workspace_root")).resolve(strict=True)
        executable = _absolute(data.get("ty_executable"))
        if not root.is_dir() or not executable.is_file():
            raise AdapterError(
                "INVALID_INPUT", "Workspace or preinstalled ty executable is missing"
            )
        enabled, roots, state = _authority(
            data.get("mutations", {}), data.get("state_directory"), root
        )
        return Config(
            workspace_root=root,
            ty_executable=executable,
            state_directory=state,
            writable_roots=roots,
            mutations_enabled=enabled,
            request_timeout_seconds=_timeout(data.get("request_timeout_seconds", 20)),
            initialize_timeout_seconds=_timeout(data.get("initialize_timeout_seconds", 20)),
            shutdown_timeout_seconds=_timeout(data.get("shutdown_timeout_seconds", 3)),
            kill_timeout_seconds=_timeout(data.get("kill_timeout_seconds", 2)),
            limits=_limits(data.get("limits", {})),
            exclusions=_relative_paths(data.get("exclusions", [])),
            project_config_files=_relative_paths(
                data.get("project_config_files", ["pyproject.toml", "ty.toml"])
            ),
        )
    except (OSError, ValueError, UnicodeError, TypeError, RecursionError, OverflowError) as error:
        raise AdapterError("INVALID_INPUT", "Unable to load valid JSON settings") from error
