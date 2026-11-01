"""Small POSIX descriptor boundary; unsupported platforms fail before IO."""

import ctypes
import hashlib
import importlib
import os
import stat
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from gz_mcp_lsp.config import write_platform_supported
from gz_mcp_lsp.models import AdapterError, FileIdentity


def require_platform() -> None:
    """No weakened path-based fallback for missing safety primitives."""
    required = ("O_DIRECTORY", "O_NOFOLLOW", "O_CLOEXEC", "geteuid")
    if (
        not write_platform_supported()
        or any(not hasattr(os, name) for name in required)
        or not {os.open, os.stat, os.unlink, os.rename, os.mkdir} <= os.supports_dir_fd
        or os.listdir not in os.supports_fd
    ):
        raise AdapterError("UNSUPPORTED", "Guarded local POSIX writes are unavailable")


def directory(path: Path) -> int:
    """Pin every absolute path component without following symlinks."""
    if not path.is_absolute() or ".." in path.parts:
        raise AdapterError("OUTSIDE_WORKSPACE", "Directory must be absolute and nontraversing")
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    flags |= getattr(os, "O_CLOEXEC", 0)
    descriptor = os.open(path.anchor, flags)
    try:
        for name in path.parts[1:]:
            child = os.open(name, flags, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


@contextmanager
def opened_directory(path: Path):
    descriptor = directory(path)
    try:
        yield descriptor
    finally:
        os.close(descriptor)


def uid() -> int:
    getter = getattr(os, "geteuid", None)
    if getter is None:
        raise AdapterError("UNSUPPORTED", "POSIX user identity is unavailable")
    return getter()


def identity(info: os.stat_result) -> dict[str, int]:
    return {
        "device": info.st_dev,
        "inode": info.st_ino,
        "mode": info.st_mode,
        "links": info.st_nlink,
    }


def same_directory(left: os.stat_result, right: os.stat_result) -> bool:
    return (left.st_dev, left.st_ino) == (right.st_dev, right.st_ino)


def private_directory(descriptor: int) -> None:
    info = os.fstat(descriptor)
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != uid() or info.st_mode & 0o077:
        raise AdapterError("RECOVERY_REQUIRED", "Recovery storage is not operator-private")


def local_filesystem(descriptor: int) -> None:
    """Use the fixed 64-bit Linux/Darwin statfs ABI; reject remote/unknown types."""
    libc = ctypes.CDLL(None, use_errno=True)
    if sys.platform == "darwin":
        function = getattr(libc, "fstatfs$INODE64", None) or getattr(libc, "fstatfs64", None)
    else:
        function = getattr(libc, "fstatfs", None)
    if function is None:
        raise AdapterError("UNSUPPORTED", "Local filesystem identity is unavailable")
    # Linux x86_64 statfs: 120 bytes. Darwin statfs64: 2168 bytes, type name offset 72.
    buffer = ctypes.create_string_buffer(4096)
    function.argtypes = [ctypes.c_int, ctypes.c_void_p]
    function.restype = ctypes.c_int
    if function(descriptor, buffer) != 0:
        raise AdapterError("UNSUPPORTED", "Unable to establish local filesystem identity")
    if sys.platform == "darwin":
        supported = buffer.raw[72:88].split(b"\0", 1)[0] in {b"apfs", b"hfs"}
    else:
        supported = ctypes.c_long.from_buffer(buffer).value in {0xEF53, 0x58465342, 0x9123683E}
    if not supported:
        raise AdapterError("UNSUPPORTED", "Filesystem is not a verified durable local write target")


def sync(descriptor: int, *, is_directory: bool = False) -> None:
    os.fsync(descriptor)
    if sys.platform == "darwin" and not is_directory:
        fcntl = _fcntl()
        fcntl.fcntl(descriptor, fcntl.F_FULLFSYNC)


@contextmanager
def locked(descriptor: int):
    fcntl = _fcntl()
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError as error:
        raise AdapterError(
            "WORKSPACE_BUSY", "Recovery state is owned by another writer", True
        ) from error
    try:
        yield
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)


def read_file(
    parent: int, name: str, limit: int, *, private: bool = False
) -> tuple[bytes, os.stat_result]:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    descriptor = os.open(name, flags | getattr(os, "O_CLOEXEC", 0), dir_fd=parent)
    with os.fdopen(descriptor, "rb") as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise AdapterError(
                "RECOVERY_REQUIRED" if private else "CONFLICT", "Unsafe regular-file identity"
            )
        if private and before.st_uid != uid():
            raise AdapterError("RECOVERY_REQUIRED", "Recovery file has an unexpected owner")
        data = stream.read(limit + 1)
        after = os.fstat(stream.fileno())
    if len(data) > limit:
        raise AdapterError("LIMIT_EXCEEDED", "Saved file exceeds its byte budget")
    if (
        FileIdentity.from_stat(before) != FileIdentity.from_stat(after)
        or before.st_mtime_ns != after.st_mtime_ns
        or before.st_size != after.st_size
    ):
        raise AdapterError("CONFLICT", "File changed during descriptor read")
    return data, after


def write_file(parent: int, name: str, data: bytes, mode: int = 0o600) -> os.stat_result:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(name, flags | getattr(os, "O_CLOEXEC", 0), 0o600, dir_fd=parent)
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fchmod(stream.fileno(), mode)
        sync(stream.fileno())
        info = os.fstat(stream.fileno())
    sync(parent, is_directory=True)
    return info


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _fcntl() -> Any:
    """Keep the POSIX-only import lazy on the explicitly unsupported Windows host."""
    return importlib.import_module("fcntl")
