"""Contained saved-byte snapshots, deterministic source manifests and UTF-16 mapping."""

import hashlib
import os
import re
import stat
import time
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
                    elif path.suffix in {".py", ".pyi"} or relative.as_posix() in (
                        self.config.project_config_files
                    ):
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
