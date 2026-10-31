"""One explicit JSON configuration file; no ambient application overrides."""

import json
import os
from dataclasses import dataclass, fields
from pathlib import Path

from gz_mcp_lsp.models import AdapterError


@dataclass(frozen=True)
class Limits:
    """Reviewed resource ceilings; JSON settings may reduce them."""

    initialize_seconds: int = 20
    request_seconds: int = 20
    shutdown_seconds: int = 3
    escalation_seconds: int = 2
    max_header_bytes: int = 4096
    max_frame_bytes: int = 16 * 1024 * 1024
    max_file_bytes: int = 2 * 1024 * 1024
    max_workspace_bytes: int = 64 * 1024 * 1024
    max_files: int = 10_000
    max_result_bytes: int = 1024 * 1024
    max_inflight: int = 8
    max_edit_files: int = 100
    max_edits: int = 1000
    max_staged_bytes: int = 8 * 1024 * 1024
    max_state_bytes: int = 256 * 1024 * 1024


@dataclass(frozen=True)
class Config:
    """Validated operator-selected workspace, executable and write authority."""

    workspace_root: Path
    ty_executable: Path
    state_directory: Path | None = None
    writable_roots: tuple[Path, ...] = ()
    mutations_enabled: bool = False
    limits: Limits = Limits()
    exclusions: tuple[str, ...] = ()
    project_inputs: tuple[str, ...] = ()


def object_value(value: object, allowed: set[str]) -> dict:
    """Reject unknown settings instead of silently accepting misspelled policy."""
    if not isinstance(value, dict) or set(value) - allowed:
        raise AdapterError("INVALID_INPUT", "Unknown or malformed configuration setting")
    return value


def absolute_path(value: object) -> Path:
    """Require an explicit absolute path independent of the process cwd."""
    if not isinstance(value, str) or not value or "\x00" in value:
        raise AdapterError("INVALID_INPUT", "Expected an absolute path")
    path = Path(value)
    if not path.is_absolute() or ".." in path.parts:
        raise AdapterError("INVALID_INPUT", "Expected an absolute path without traversal")
    return path


def relative_paths(value: object) -> tuple[str, ...]:
    """Validate bounded scope inputs without glob or gitignore interpretation."""
    if not isinstance(value, list) or len(value) > 100:
        raise AdapterError("INVALID_INPUT", "Expected at most 100 relative scope paths")
    result = []
    for item in value:
        if not isinstance(item, str) or not item or "\x00" in item:
            raise AdapterError("INVALID_INPUT", "Invalid scope path")
        path = Path(item)
        if path.is_absolute() or ".." in path.parts or str(path) == ".":
            raise AdapterError("INVALID_INPUT", "Scope paths must stay within the workspace")
        result.append(path.as_posix())
    return tuple(result)


def parse_limits(payload: dict) -> Limits:
    """Apply reviewed positive-integer reductions to the fixed resource policy."""
    defaults = Limits()
    values = object_value(payload.get("limits", {}), {field.name for field in fields(Limits)})
    values = dict(values)
    if "request_timeout_seconds" in payload:
        if "request_seconds" in values:
            raise AdapterError("INVALID_INPUT", "Specify request timeout only once")
        values["request_seconds"] = payload["request_timeout_seconds"]
    for name, value in values.items():
        if type(value) is not int or not 0 < value <= getattr(defaults, name):
            raise AdapterError("INVALID_INPUT", "Resource limits require positive bounded integers")
    return Limits(**values)


def parse_config(payload: object) -> Config:
    """Validate the whole configuration before any subprocess or filesystem write."""
    data = object_value(
        payload,
        {
            "schema_version",
            "workspace_root",
            "ty_executable",
            "state_directory",
            "mutations",
            "limits",
            "exclusions",
            "project_inputs",
            "request_timeout_seconds",
        },
    )
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise AdapterError("INVALID_INPUT", "Unsupported configuration schema")
    root = absolute_path(data.get("workspace_root")).resolve()
    executable = absolute_path(data.get("ty_executable"))
    if not root.is_dir() or not executable.is_file() or not os.access(executable, os.X_OK):
        raise AdapterError("INVALID_INPUT", "Workspace or language-server executable unavailable")
    mutations = object_value(data.get("mutations", {}), {"enabled", "writable_roots"})
    enabled = mutations.get("enabled", False)
    if type(enabled) is not bool:
        raise AdapterError("INVALID_INPUT", "Mutation enablement must be boolean")
    raw_roots = mutations.get("writable_roots", [])
    if not isinstance(raw_roots, list) or len(raw_roots) > 100:
        raise AdapterError("INVALID_INPUT", "Invalid writable roots")
    roots = tuple(absolute_path(item) for item in raw_roots)
    for writable in roots:
        if (
            not writable.is_dir()
            or writable.is_symlink()
            or not writable.resolve().is_relative_to(root)
        ):
            raise AdapterError(
                "OUTSIDE_WORKSPACE", "Writable root is not authorized workspace storage"
            )
    state = absolute_path(data["state_directory"]) if "state_directory" in data else None
    if state is not None and state.resolve().is_relative_to(root):
        raise AdapterError("INVALID_INPUT", "Recovery storage must be outside the source workspace")
    if enabled and (not roots or state is None):
        raise AdapterError("INVALID_INPUT", "Writes require explicit roots and recovery storage")
    return Config(
        root,
        executable,
        state,
        roots,
        enabled,
        parse_limits(data),
        relative_paths(data.get("exclusions", [])),
        relative_paths(data.get("project_inputs", [])),
    )


def unique_object(items: list[tuple[str, object]]) -> dict:
    """Reject duplicate JSON keys that could conceal conflicting operator policy."""
    result = {}
    for key, value in items:
        if key in result:
            raise AdapterError("INVALID_INPUT", "Duplicate configuration key")
        result[key] = value
    return result


def load_config(path: Path) -> Config:
    """Read one bounded JSON settings file and normalize operational failures."""
    try:
        with path.open("rb") as stream:
            content = stream.read(64 * 1024 + 1)
        if len(content) > 64 * 1024:
            raise AdapterError("LIMIT_EXCEEDED", "Configuration is too large")
        return parse_config(json.loads(content, object_pairs_hook=unique_object))
    except (OSError, ValueError, UnicodeError, RecursionError) as error:
        raise AdapterError("INVALID_INPUT", "Cannot read valid JSON configuration") from error
