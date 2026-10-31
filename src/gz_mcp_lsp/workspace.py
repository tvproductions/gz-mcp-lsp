"""Saved workspace identity, bounded reads and precise UTF-16 byte mappings."""

import hashlib
import os
import re
import stat
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import unquote_to_bytes, urlsplit

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.coordinates import byte_offset
from gz_mcp_lsp.models import AdapterError, FileIdentity, Position, Snapshot

BLOCKED_DIRECTORIES = {".git", ".venv", "__pycache__", "node_modules", ".superpowers"}


def file_identity(info: os.stat_result) -> FileIdentity:
    """Retain ownership as well as object, link and permission identity."""
    return FileIdentity(
        info.st_dev,
        info.st_ino,
        info.st_mode,
        0 if stat.S_ISDIR(info.st_mode) else info.st_nlink,
        info.st_uid,
        info.st_gid,
    )


class Workspace:
    """Read local authorized snapshots without interpreting source as executable code."""

    def __init__(self, config: Config):
        self.config = config
        self.root = config.workspace_root
        root_stat = self.root.stat()
        self._root_identity = (root_stat.st_dev, root_stat.st_ino)

    def path(self, uri: str) -> Path:
        """Validate local URI identity without following source symlinks."""
        if not isinstance(uri, str) or re.search(r"%(?![0-9a-fA-F]{2})", uri):
            raise AdapterError("INVALID_INPUT", "Malformed file URI")
        try:
            parsed = urlsplit(uri)
            decoded = unquote_to_bytes(parsed.path).decode("utf-8", errors="strict")
        except (ValueError, UnicodeError) as error:
            raise AdapterError("INVALID_INPUT", "Malformed file URI") from error
        if (
            parsed.scheme != "file"
            or parsed.netloc
            or parsed.query
            or parsed.fragment
            or "\x00" in decoded
        ):
            raise AdapterError(
                "INVALID_INPUT", "Expected a local file URI without query or fragment"
            )
        path = Path(decoded)
        if not path.is_absolute() or ".." in path.parts or not path.is_relative_to(self.root):
            raise AdapterError("OUTSIDE_WORKSPACE", "Document is outside the workspace")
        relative = path.relative_to(self.root)
        if self.excluded(path):
            raise AdapterError("OUTSIDE_WORKSPACE", "Document is excluded by operator scope")
        current = self.root
        try:
            for part in relative.parts:
                if part in BLOCKED_DIRECTORIES or part.startswith(".gz-mcp-lsp-"):
                    raise AdapterError("OUTSIDE_WORKSPACE", "Excluded workspace storage")
                current /= part
                if stat.S_ISLNK(current.lstat().st_mode):
                    raise AdapterError("OUTSIDE_WORKSPACE", "Source symlinks are not authorized")
        except OSError as error:
            raise AdapterError("SOURCE_UNAVAILABLE", "Document is not readable") from error
        return path

    @contextmanager
    def parent_handle(self, path: Path):
        """Yield the anchored parent handle and every directory identity in its chain."""
        if os.open not in os.supports_dir_fd or not hasattr(os, "O_NOFOLLOW"):
            raise AdapterError("UNSUPPORTED", "Guarded directory handles unavailable")
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        parent = os.open(self.root, flags)
        try:
            info = os.fstat(parent)
            if (info.st_dev, info.st_ino) != self._root_identity:
                raise AdapterError("STALE_DOCUMENT", "Workspace root identity changed", True)
            identities = [file_identity(info)]
            parts = path.relative_to(self.root).parts
            if not parts:
                raise AdapterError("INVALID_INPUT", "Document must be a file")
            for part in parts[:-1]:
                child = os.open(part, flags, dir_fd=parent)
                os.close(parent)
                parent = child
                identities.append(file_identity(os.fstat(parent)))
            yield parent, tuple(identities)
        finally:
            os.close(parent)

    def open_source(self, path: Path, parents: list[FileIdentity]) -> int:
        """Open a no-follow source descriptor and retain its parent identity chain."""
        with self.parent_handle(path) as (parent, identities):
            parents.extend(identities)
            return os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)

    def read(self, uri: str) -> Snapshot:
        """Read a regular UTF-8 file with size bounds and detectable-race checks."""
        path = self.path(uri)
        try:
            parents = []
            descriptor = self.open_source(path, parents)
            with os.fdopen(descriptor, "rb") as stream:
                before = os.fstat(stream.fileno())
                if not stat.S_ISREG(before.st_mode):
                    raise AdapterError("INVALID_INPUT", "Document must be a regular file")
                data = stream.read(self.config.limits.max_file_bytes + 1)
                after = os.fstat(stream.fileno())
            current = path.lstat()
            if self.stamp(before) != self.stamp(after) or self.stamp(after) != self.stamp(current):
                raise AdapterError("STALE_DOCUMENT", "Document changed while reading", True)
            if len(data) > self.config.limits.max_file_bytes:
                raise AdapterError("LIMIT_EXCEEDED", "Document exceeds file size limit")
            data.decode("utf-8", errors="strict")
            if b"\x00" in data:
                raise AdapterError("INVALID_INPUT", "Document must be UTF-8 text")
        except (OSError, UnicodeError) as error:
            raise AdapterError("SOURCE_UNAVAILABLE", "Cannot read UTF-8 source") from error
        identity = file_identity(before)
        return Snapshot(
            path.as_uri(), data, hashlib.sha256(data).hexdigest(), 1, identity, tuple(parents)
        )

    @staticmethod
    def stamp(info: os.stat_result) -> tuple[int, ...]:
        """Compare content-relevant identity around a read, without using access time."""
        return (
            info.st_dev,
            info.st_ino,
            info.st_mode,
            info.st_nlink,
            info.st_size,
            info.st_mtime_ns,
            info.st_ctime_ns,
        )

    def offset(self, snapshot: Snapshot, position: Position) -> int:
        """Delegate exact UTF-16 mapping to the pure coordinate boundary."""
        return byte_offset(snapshot, position)

    def excluded(self, path: Path) -> bool:
        """Apply explicit relative exclusions, without fuzzy glob interpretation."""
        relative = path.relative_to(self.root)
        return any(
            relative == Path(item) or relative.is_relative_to(Path(item))
            for item in self.config.exclusions
        )

    def manifest(self) -> str:
        """Hash every eligible saved source/config input within explicit resource limits."""
        digest = hashlib.sha256()
        total = count = visited = 0
        pending = [self.root]
        while pending:
            directory = pending.pop()
            try:
                entries = []
                with os.scandir(directory) as stream:
                    for entry in stream:
                        visited += 1
                        if visited > self.config.limits.max_files * 4:
                            raise AdapterError(
                                "LIMIT_EXCEEDED", "Workspace traversal exceeds limits"
                            )
                        entries.append(Path(entry.path))
                entries.sort()
                for path in entries:
                    if path.name in BLOCKED_DIRECTORIES or self.excluded(path):
                        continue
                    if path.is_symlink():
                        raise AdapterError("OUTSIDE_WORKSPACE", "Source scope contains a symlink")
                    if path.is_dir():
                        pending.append(path)
                        continue
                    relative = path.relative_to(self.root).as_posix()
                    if path.suffix not in {".py", ".pyi"} and relative not in {
                        "pyproject.toml",
                        "ty.toml",
                        *self.config.project_inputs,
                    }:
                        continue
                    snapshot = self.read(path.as_uri())
                    count += 1
                    total += len(snapshot.data)
                    if (
                        count > self.config.limits.max_files
                        or total > self.config.limits.max_workspace_bytes
                    ):
                        raise AdapterError(
                            "LIMIT_EXCEEDED", "Workspace source scope exceeds limits"
                        )
                    digest.update(relative.encode("utf-8") + b"\0")
                    digest.update(snapshot.sha256.encode("ascii"))
                    digest.update(str(snapshot.identity).encode("ascii"))
            except OSError as error:
                raise AdapterError(
                    "WORKSPACE_BUSY", "Workspace scope is not readable", True
                ) from error
        return digest.hexdigest()
