"""Contained saved-byte snapshots, deterministic source manifests and UTF-16 mapping."""

import hashlib
import os
import re
import stat
import time
import tomllib
from collections.abc import Iterator
from pathlib import Path
from urllib.parse import unquote_to_bytes, urlsplit

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.models import AdapterError, FileIdentity, Position, Snapshot

_DENIED_COMPONENTS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    ".tox",
    ".nox",
    "site-packages",
    "node_modules",
    "__pycache__",
    ".superpowers",
    ".gz-mcp-lsp-state",
}


class Workspace:
    """Read one configured source scope without executing workspace code."""

    def __init__(self, config: Config):
        self.config = config
        self.root = config.workspace_root

    def _excluded(self, relative: Path) -> bool:
        if any(part in _DENIED_COMPONENTS for part in relative.parts):
            return True
        return any(relative.is_relative_to(Path(item)) for item in self.config.exclusions)

    @staticmethod
    def _checked_stat(path: Path) -> os.stat_result:
        info = path.lstat()
        reparse = getattr(info, "st_file_attributes", 0) & getattr(
            stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0
        )
        if stat.S_ISLNK(info.st_mode) or reparse:
            raise AdapterError("OUTSIDE_WORKSPACE", "Symlinks and reparse points are not source")
        return info

    def path(self, uri: str) -> Path:
        """Decode exactly once, reject aliases that escape, and check every component."""
        if not isinstance(uri, str) or "?" in uri or "#" in uri:
            raise AdapterError(
                "INVALID_INPUT", "Expected a local file URI without query or fragment"
            )
        try:
            parsed = urlsplit(uri)
            if parsed.scheme != "file" or parsed.netloc or re.search(r"%(?![0-9a-fA-F]{2})", uri):
                raise AdapterError("INVALID_INPUT", "Malformed or nonlocal file URI")
            decoded = unquote_to_bytes(parsed.path).decode("utf-8")
            if "\0" in decoded or "\\" in decoded or decoded.startswith("//"):
                raise AdapterError("INVALID_INPUT", "Malformed local URI path")
            if any(part in {".", ".."} for part in decoded.split("/")):
                raise AdapterError("OUTSIDE_WORKSPACE", "Traversal is not permitted")
            if os.name == "nt":
                if not re.match(r"^/[a-zA-Z]:/", decoded):
                    raise AdapterError(
                        "INVALID_INPUT", "Windows URI requires an absolute drive path"
                    )
                decoded = decoded[1:]
            path = Path(decoded)
            if not path.is_absolute() or not path.is_relative_to(self.root):
                raise AdapterError("OUTSIDE_WORKSPACE", "Source is outside the workspace")
            relative = path.relative_to(self.root)
            if self._excluded(relative):
                raise AdapterError("OUTSIDE_WORKSPACE", "Source is excluded by workspace policy")
            current = self.root
            self._checked_stat(current)
            for part in relative.parts:
                current = current / part
                self._checked_stat(current)
            if not stat.S_ISREG(self._checked_stat(path).st_mode):
                raise AdapterError("INVALID_INPUT", "Source must be a regular file")
            return path
        except (OSError, ValueError, UnicodeError) as error:
            raise AdapterError(
                "SOURCE_UNAVAILABLE", "Unable to read a valid source path"
            ) from error

    def source_scope(self, uri: str) -> str:
        """Classify target metadata without ever reading an external source."""
        try:
            parsed = urlsplit(uri)
        except ValueError as error:
            raise AdapterError("PROTOCOL_ERROR", "Malformed target URI") from error
        if parsed.scheme != "file" or parsed.netloc:
            return "external"
        try:
            self.path(uri)
        except AdapterError as error:
            if error.code == "OUTSIDE_WORKSPACE":
                return "external"
            if error.code in {"SOURCE_UNAVAILABLE", "INVALID_INPUT"}:
                return "unavailable"
            raise
        return "workspace"

    def canonical_uri(self, uri: str) -> str:
        """Normalize encoded aliases for identity keys, preserving caller URI in snapshots."""
        path = self.path(uri).resolve(strict=True)
        self.path(path.as_uri())
        return path.as_uri()

    def read(self, uri: str) -> Snapshot:
        """Read bounded exact bytes through one verified regular-file descriptor."""
        path = self.path(uri)
        before = self._checked_stat(path)
        flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOFOLLOW", 0)
        flags |= getattr(os, "O_BINARY", 0)
        try:
            descriptor = os.open(path, flags)
            with os.fdopen(descriptor, "rb") as source:
                opened = os.fstat(source.fileno())
                if not stat.S_ISREG(opened.st_mode):
                    raise AdapterError("INVALID_INPUT", "Source must remain a regular file")
                if FileIdentity.from_stat(opened) != FileIdentity.from_stat(before):
                    raise AdapterError("STALE_DOCUMENT", "Source identity changed while opening")
                self.path(uri)
                data = source.read(self.config.limits.file_bytes + 1)
                after = os.fstat(source.fileno())
            if len(data) > self.config.limits.file_bytes:
                raise AdapterError("LIMIT_EXCEEDED", "Source exceeds the file byte limit")
            if (after.st_size, after.st_mtime_ns) != (opened.st_size, opened.st_mtime_ns):
                raise AdapterError("STALE_DOCUMENT", "Source changed while reading")
            data.decode("utf-8")
            self.path(uri)
            return Snapshot(
                uri, data, hashlib.sha256(data).hexdigest(), 1, FileIdentity.from_stat(after)
            )
        except (OSError, UnicodeError) as error:
            raise AdapterError(
                "SOURCE_UNAVAILABLE", "Source is unavailable or not UTF-8"
            ) from error

    def tracked(self, path: Path) -> bool:
        """One predicate defines both scan membership and semantic document admission."""
        if not path.is_relative_to(self.root):
            return False
        relative = path.relative_to(self.root)
        return not self._excluded(relative) and (
            path.suffix in {".py", ".pyi"}
            or path.name in {"pyproject.toml", "ty.toml", ".gitignore", ".ignore"}
            or relative.as_posix() in self.config.project_config_files
        )

    def _eligible(self) -> Iterator[Path]:
        pending = [self.root]
        deadline = time.monotonic() + self.config.request_timeout_seconds
        while pending:
            directory = pending.pop()
            self._checked_stat(directory)
            with os.scandir(directory) as entries:
                for entry in entries:
                    if time.monotonic() > deadline:
                        raise AdapterError("TIMEOUT", "Workspace scan exceeded its budget")
                    path = Path(entry.path)
                    relative = path.relative_to(self.root)
                    if self._excluded(relative):
                        continue
                    info = self._checked_stat(path)
                    if stat.S_ISDIR(info.st_mode):
                        pending.append(path)
                        if len(pending) > self.config.limits.workspace_files:
                            raise AdapterError("LIMIT_EXCEEDED", "Too many source directories")
                    elif self.tracked(path):
                        yield path

    def manifest(self) -> str:
        """Hash content and identity, including unopened files and project configuration."""
        records = []
        total = 0
        try:
            for path in self._eligible():
                snapshot = self.read(path.as_uri())
                total += len(snapshot.data)
                if len(records) >= self.config.limits.workspace_files:
                    raise AdapterError("LIMIT_EXCEEDED", "Workspace has too many eligible files")
                if total > self.config.limits.workspace_bytes:
                    raise AdapterError("LIMIT_EXCEEDED", "Workspace exceeds its source byte budget")
                relative = path.relative_to(self.root).as_posix()
                records.append((relative, snapshot.sha256, repr(snapshot.identity)))
        except OSError as error:
            raise AdapterError(
                "WORKSPACE_BUSY", "Workspace scope changed or cannot be scanned"
            ) from error
        return hashlib.sha256(repr(sorted(records)).encode("utf-8")).hexdigest()

    def semantic_manifest(self) -> str:
        """Reject ty scope we cannot reconcile before claiming semantic freshness."""

        if self.config.exclusions:
            raise AdapterError(
                "UNSUPPORTED", "Custom source exclusions are not reconciled with ty indexing"
            )
        # These locate ty's native configuration, never product settings overrides.
        if os.name == "nt":
            native_base = Path(os.environ.get("APPDATA", str(Path.home() / "AppData/Roaming")))
        else:
            native_base = Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config")))
        external = [native_base / "ty/ty.toml"]
        for parent in self.root.parents:
            external.extend((parent / "ty.toml", parent / "pyproject.toml"))
        if any(path.exists() or path.is_symlink() for path in external):
            raise AdapterError(
                "UNSUPPORTED", "Inherited or user ty configuration is outside the tracked scope"
            )
        total = 0
        count = 0
        for path in self._eligible():
            if path.name not in {"pyproject.toml", "ty.toml"}:
                continue
            snapshot = self.read(path.as_uri())
            count += 1
            total += len(snapshot.data)
            if (
                count > self.config.limits.workspace_files
                or total > self.config.limits.workspace_bytes
            ):
                raise AdapterError(
                    "LIMIT_EXCEEDED", "Project configuration exceeds its scope budget"
                )
            try:
                raw = tomllib.loads(snapshot.data.decode("utf-8"))
                settings = raw if path.name == "ty.toml" else raw.get("tool", {}).get("ty", {})
                self._check_ty_roots(settings, path.parent)
            except (tomllib.TOMLDecodeError, AttributeError, TypeError) as error:
                raise AdapterError(
                    "UNSUPPORTED", "Unable to establish project configuration scope"
                ) from error
        return self.manifest()

    def _check_ty_roots(self, settings: object, base: Path) -> None:
        if not isinstance(settings, dict):
            raise AdapterError("UNSUPPORTED", "Invalid ty project configuration")
        self._check_ty_patterns(settings.get("src", {}))
        baseline = settings.get("baseline")
        if baseline is not None and baseline not in self.config.project_config_files:
            raise AdapterError(
                "UNSUPPORTED", "Baseline must be an explicitly tracked configuration input"
            )
        self._check_ty_environment(settings.get("environment", {}), base)

    @staticmethod
    def _check_ty_patterns(source: object) -> None:
        """Reject source globs that can escape or expand outside tracked inputs."""

        if not isinstance(source, dict):
            raise AdapterError("UNSUPPORTED", "Invalid ty source configuration")
        for field in ("include", "exclude"):
            patterns = source.get(field, [])
            if not isinstance(patterns, list):
                raise AdapterError("UNSUPPORTED", "Invalid ty source patterns")
            for pattern in patterns:
                if (
                    not isinstance(pattern, str)
                    or Path(pattern).is_absolute()
                    or ".." in pattern.split("/")
                    or "\\" in pattern
                    or "$" in pattern
                    or "~" in pattern
                ):
                    raise AdapterError("UNSUPPORTED", "Untracked ty source pattern")

    def _check_ty_environment(self, environment: object, base: Path) -> None:
        """Keep first-party roots confined and custom typeshed outside the contract."""

        if not isinstance(environment, dict):
            raise AdapterError("UNSUPPORTED", "Invalid ty environment configuration")
        for key in ("root", "extra-paths"):
            values = environment.get(key, [])
            if not isinstance(values, list):
                raise AdapterError("UNSUPPORTED", "Invalid ty source roots")
            for value in values:
                if not isinstance(value, str) or any(char in value for char in "$~"):
                    raise AdapterError("UNSUPPORTED", "Unresolved ty source root")
                candidate = (base / value).resolve()
                if not candidate.is_relative_to(self.root) or self._excluded(
                    candidate.relative_to(self.root)
                ):
                    raise AdapterError("UNSUPPORTED", "Untracked ty first-party source root")
        if environment.get("typeshed") is not None:
            raise AdapterError("UNSUPPORTED", "Custom typeshed scope is not tracked")

    @staticmethod
    def offset(snapshot: Snapshot, position: Position) -> int:
        """Convert a validated UTF-16 position to a byte offset without clamping."""
        start = 0
        line = 0
        for delimiter in re.finditer(rb"\r\n|\r|\n", snapshot.data):
            if line == position.line:
                return start + _line_offset(
                    snapshot.data[start : delimiter.start()], position.character
                )
            line += 1
            start = delimiter.end()
        if line == position.line:
            return start + _line_offset(snapshot.data[start:], position.character)
        raise AdapterError("INVALID_INPUT", "Position line is outside the document")


def _line_offset(data: bytes, character: int) -> int:
    units = 0
    offset = 0
    for value in data.decode("utf-8"):
        if units == character:
            return offset
        units += 2 if ord(value) > 0xFFFF else 1
        if units > character:
            raise AdapterError("INVALID_INPUT", "Position splits a UTF-16 surrogate pair")
        offset += len(value.encode("utf-8"))
    if units == character:
        return offset
    raise AdapterError("INVALID_INPUT", "Position character is outside the line")
