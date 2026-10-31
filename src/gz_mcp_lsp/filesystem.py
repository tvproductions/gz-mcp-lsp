"""Guarded local POSIX replacement, durable receipts and conservative crash recovery."""

import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import time
from contextlib import ExitStack, suppress
from dataclasses import asdict
from pathlib import Path

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.edit_plan import EditPlan, edit_uri
from gz_mcp_lsp.models import AdapterError, FileIdentity, Json
from gz_mcp_lsp.workspace import Workspace, file_identity

type TransactionReceipt = dict[str, Json]
HEX = re.compile(r"[0-9a-f]{64}\Z")
TERMINAL = {"committed", "no_op", "rolled_back", "recovery_required"}
MAX_JOURNAL = 1024 * 1024


def digest(data: bytes) -> str:
    """Hash exact saved/staged bytes."""
    return hashlib.sha256(data).hexdigest()


def local_volume(path: Path) -> bool:
    """Restrict the initial adapter to recognized local filesystems."""
    if sys.platform == "darwin":
        result = subprocess.run(
            ["/sbin/mount"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="surrogateescape",
            check=True,
            timeout=2,
        )
        if len(result.stdout) > 1024 * 1024:
            return False
        candidates = []
        for line in result.stdout.splitlines():
            prefix, separator, flags = line.rpartition(" (")
            _, on, mount = prefix.partition(" on ")
            if separator and on:
                options = flags.rstrip(")").split(", ")
                point = Path(mount)
                if path.is_relative_to(point):
                    candidates.append((len(point.parts), options))
        return bool(
            candidates and max(candidates)[1][0] == "apfs" and "local" in max(candidates)[1]
        )
    if sys.platform == "linux":
        with Path("/proc/self/mountinfo").open(encoding="utf-8") as stream:
            data = stream.read(1024 * 1024 + 1)
        if len(data) > 1024 * 1024:
            return False
        candidates = []
        for line in data.splitlines():
            before, separator, after = line.partition(" - ")
            fields = before.split()
            if separator and len(fields) >= 5:
                point = Path(re.sub(r"\\([0-7]{3})", lambda m: chr(int(m[1], 8)), fields[4]))
                if path.is_relative_to(point):
                    candidates.append((len(point.parts), after.split()[0]))
        return bool(
            candidates and max(candidates)[1] in {"ext4", "xfs", "btrfs", "tmpfs", "overlay"}
        )
    return False


def read_at(parent: int, name: str, maximum: int) -> tuple[bytes, FileIdentity]:
    """Read one regular unlinked-alias-free object through an anchored handle."""
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
    with os.fdopen(fd, "rb") as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise AdapterError("RECOVERY_REQUIRED", "Unsafe staged/state object")
        data = stream.read(maximum + 1)
        after = os.fstat(stream.fileno())
        if len(data) > maximum or Workspace.stamp(before) != Workspace.stamp(after):
            raise AdapterError("RECOVERY_REQUIRED", "Staged/state object exceeds bounds or changed")
        return data, file_identity(after)


def write_at(
    parent: int, name: str, data: bytes, mode: int = 0o600, group: int = -1
) -> FileIdentity:
    """Create exclusively, preserve requested group/mode and durably flush before use."""
    fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=parent)
    with os.fdopen(fd, "wb") as stream:
        stream.write(data)
        if group >= 0:
            os.fchown(stream.fileno(), os.getuid(), group)
        os.fchmod(stream.fileno(), stat.S_IMODE(mode))
        stream.flush()
        os.fsync(stream.fileno())
        return file_identity(os.fstat(stream.fileno()))


def directory(path: Path) -> int:
    """Open/create only the final state directory without following any ancestor link."""
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    fd = os.open("/", flags)
    try:
        for index, part in enumerate(path.parts[1:]):
            if index == len(path.parts) - 2:
                with suppress(FileExistsError):
                    os.mkdir(part, 0o700, dir_fd=fd)
            child = os.open(part, flags, dir_fd=fd)
            os.close(fd)
            fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise


class _State:
    """Private, single-writer journal directory with a durable registered-ID index."""

    def __init__(self, config: Config):
        self.fd = self.lock = -1
        self.ids: list[str] = []
        self.config = config
        try:
            assert config.state_directory is not None
            self.fd = directory(config.state_directory)
            info = os.fstat(self.fd)
            if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o700:
                raise AdapterError(
                    "RECOVERY_REQUIRED", "State directory must be private and owned by the operator"
                )
            self.lock = os.open(
                ".lock", os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600, dir_fd=self.fd
            )
            lock_info = os.fstat(self.lock)
            if (
                not stat.S_ISREG(lock_info.st_mode)
                or lock_info.st_nlink != 1
                or lock_info.st_uid != os.getuid()
            ):
                raise AdapterError("RECOVERY_REQUIRED", "Unsafe state lock")
            import fcntl

            try:
                fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as error:
                raise AdapterError(
                    "WORKSPACE_BUSY", "Another adapter owns mutation state", True
                ) from error
            self._load_index()
        except BaseException:
            self.close()
            raise

    def _load_index(self) -> None:
        """Validate retained state only after acquiring its exclusive lifetime lock."""
        names = self.names()
        for name in names:
            if name.endswith(".tmp"):
                read_at(self.fd, name, MAX_JOURNAL)
                os.unlink(name, dir_fd=self.fd)
        names = self.names()
        if ".index.json" not in names:
            if names != [".lock"]:
                raise AdapterError("RECOVERY_REQUIRED", "State index is missing")
            self.write(".index.json", {"schema_version": 1, "ids": []})
        index = self.read(".index.json")
        ids = index.get("ids")
        if (
            index.get("schema_version") != 1
            or not isinstance(ids, list)
            or len(ids) > self.config.limits.max_files
            or any(not isinstance(value, str) or not HEX.fullmatch(value) for value in ids)
            or len(set(ids)) != len(ids)
        ):
            raise AdapterError("RECOVERY_REQUIRED", "Invalid state index")
        self.ids = ids
        expected = {".lock", ".index.json", *(f"{value}.json" for value in ids)}
        if set(self.names()) != expected:
            raise AdapterError("RECOVERY_REQUIRED", "Missing or unexpected registered state")

    def names(self) -> list[str]:
        """Bound state entry enumeration before allocating an unbounded listing."""
        names = []
        with os.scandir(self.fd) as stream:
            for entry in stream:
                names.append(entry.name)
                if len(names) > self.config.limits.max_files + 4:
                    raise AdapterError(
                        "LIMIT_EXCEEDED", "Retained transaction count exceeds state limits"
                    )
        return sorted(names)

    def read(self, name: str) -> dict:
        """Malformed/missing private metadata is recovery failure, not empty history."""
        try:
            data, identity = read_at(self.fd, name, MAX_JOURNAL)
            if identity.owner != os.getuid() or stat.S_IMODE(identity.mode) != 0o600:
                raise ValueError("Nonprivate state object")
            value = json.loads(data)
            if not isinstance(value, dict):
                raise ValueError("Expected state object")
            return value
        except OSError, ValueError, UnicodeError, RecursionError:
            raise AdapterError(
                "RECOVERY_REQUIRED", "Missing or corrupt private transaction state"
            ) from None

    def write(self, name: str, value: dict) -> None:
        """Atomically replace metadata and fsync its directory before reporting durability."""
        data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
        if len(data) > MAX_JOURNAL:
            raise AdapterError("LIMIT_EXCEEDED", "Journal exceeds metadata limits")
        temporary = f".{name}.tmp"
        try:
            write_at(self.fd, temporary, data)
            os.replace(temporary, name, src_dir_fd=self.fd, dst_dir_fd=self.fd)
            os.fsync(self.fd)
        finally:
            with suppress(FileNotFoundError):
                os.unlink(temporary, dir_fd=self.fd)

    def usage(self) -> int:
        """Account for retained private metadata without following state links."""
        total = 0
        for name in self.names():
            info = os.stat(name, dir_fd=self.fd, follow_symlinks=False)
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                raise AdapterError("RECOVERY_REQUIRED", "Unsafe state object")
            total += info.st_size
        return total

    def register(self, plan_id: str) -> None:
        """Register first so missing journals can never silently erase an applied transaction."""
        if len(self.ids) >= self.config.limits.max_files:
            raise AdapterError("LIMIT_EXCEEDED", "Retained receipt capacity exhausted")
        self.ids.append(plan_id)
        self.write(".index.json", {"schema_version": 1, "ids": self.ids})

    def close(self) -> None:
        """Release the lifetime advisory lock and directory handle exactly once."""
        for name in ("lock", "fd"):
            fd = getattr(self, name)
            if fd >= 0:
                os.close(fd)
                setattr(self, name, -1)


class Transactions:
    """One authorized writer, all-target preflight, recoverable replacement and durable replay."""

    def __init__(self, config: Config, workspace: Workspace):
        self.config, self.workspace = config, workspace
        self.blocked = False
        self._state: _State | None = None
        if (
            not config.mutations_enabled
            or not config.writable_roots
            or config.state_directory is None
        ):
            raise AdapterError(
                "MUTATIONS_DISABLED", "Operator has not delegated mutation authority"
            )
        # CPython exposes directory-relative replace through its rename implementation.
        if (
            os.name != "posix"
            or not hasattr(os, "O_NOFOLLOW")
            or os.rename not in os.supports_dir_fd
        ):
            raise AdapterError("UNSUPPORTED", "Guarded POSIX replacements unavailable")
        try:
            if not local_volume(config.workspace_root) or not local_volume(
                config.state_directory.parent
            ):
                raise AdapterError(
                    "UNSUPPORTED", "Write support requires a recognized local filesystem"
                )
            self._state = _State(config)
            self.recover()
        except BaseException:
            self.close()
            raise

    @property
    def state(self) -> _State:
        """Reject use after lifetime lock release."""
        if self._state is None:
            raise AdapterError("RECOVERY_REQUIRED", "Transaction state is closed")
        return self._state

    def _checkpoint(self, event: str) -> None:
        """Fault-injection seam overridden only by disposable tests; no runtime setting."""

    def _authorize(self, uri: str):
        path = self.workspace.path(uri)
        if not any(path.is_relative_to(root) for root in self.config.writable_roots):
            raise AdapterError("OUTSIDE_WORKSPACE", "Target is outside delegated writable roots")
        if not local_volume(path.parent):
            raise AdapterError("UNSUPPORTED", "Target is not on a recognized local filesystem")
        snapshot = self.workspace.read(uri)
        if snapshot.identity.links != 1 or snapshot.identity.owner != os.getuid():
            raise AdapterError(
                "OUTSIDE_WORKSPACE", "Only operator-owned single-link files are writable"
            )
        if snapshot.identity.mode & 0o7000:
            raise AdapterError("UNSUPPORTED", "Privileged source metadata is unsupported")
        return path, snapshot

    def _journal(self, plan_id: str) -> dict:
        if not HEX.fullmatch(plan_id) or plan_id not in self.state.ids:
            raise AdapterError("PLAN_EXPIRED", "No retained transaction receipt")
        value = self.state.read(f"{plan_id}.json")
        entries = value.get("entries")
        if (
            value.get("schema_version") != 1
            or value.get("plan_id") != plan_id
            or value.get("workspace") != self.config.workspace_root.as_uri()
            or value.get("root_identity") != list(self.workspace._root_identity)
            or not isinstance(value.get("status"), str)
            or value["status"] not in {"preparing", "prepared", *TERMINAL}
            or not isinstance(entries, list)
            or len(entries) > self.config.limits.max_edit_files
        ):
            raise AdapterError("RECOVERY_REQUIRED", "Invalid transaction journal identity")
        for index, entry in enumerate(entries):
            self._validate_entry(plan_id, index, entry)
        return value

    def _validate_entry(self, plan_id: str, index: int, entry: dict) -> None:
        try:
            if not isinstance(entry, dict) or not isinstance(entry["uri"], str):
                raise ValueError("Invalid entry")
            uri = edit_uri(entry["uri"])
            if uri != entry["uri"] or not Path.from_uri(uri).is_relative_to(
                self.config.workspace_root
            ):
                raise ValueError("Invalid stored source URI")
            for key in ("before_hash", "after_hash"):
                if not isinstance(entry[key], str) or not HEX.fullmatch(entry[key]):
                    raise ValueError("Invalid hash")
            if (
                entry["before_name"] != f".gz-mcp-lsp-{plan_id}-{index}.before"
                or entry["after_name"] != f".gz-mcp-lsp-{plan_id}-{index}.after"
            ):
                raise ValueError("Invalid stage identity")
            before = self._identity(entry["before_identity"])
            if before.links != 1 or not stat.S_ISREG(before.mode):
                raise ValueError("Invalid source identity")
            if not isinstance(entry["parents"], list) or not 1 <= len(entry["parents"]) <= 1024:
                raise ValueError("Invalid directory chain")
            for parent in entry["parents"]:
                if not stat.S_ISDIR(self._identity(parent).mode):
                    raise ValueError("Invalid directory identity")
            if entry["after_identity"] is not None:
                self._identity(entry["after_identity"])
        except KeyError, TypeError, ValueError, AdapterError:
            raise AdapterError("RECOVERY_REQUIRED", "Unsafe or corrupt transaction entry") from None

    @staticmethod
    def _identity(value: dict) -> FileIdentity:
        if (
            not isinstance(value, dict)
            or set(value) != {"device", "inode", "mode", "links", "owner", "group"}
            or any(type(item) is not int or item < 0 for item in value.values())
        ):
            raise ValueError("Invalid object identity")
        return FileIdentity(**value)

    def receipt(self, plan_id: str) -> TransactionReceipt | None:
        """Look up durable outcome before preview lifetime or workspace generation checks."""
        if not isinstance(plan_id, str) or not HEX.fullmatch(plan_id):
            raise AdapterError("INVALID_INPUT", "Invalid plan identity")
        if plan_id not in self.state.ids:
            return None
        journal = self._journal(plan_id)
        if journal["status"] not in TERMINAL:
            return None
        receipt = journal.get("receipt")
        if (
            not isinstance(receipt, dict)
            or receipt.get("plan_id") != plan_id
            or receipt.get("status") != journal["status"]
        ):
            raise AdapterError("RECOVERY_REQUIRED", "Missing terminal transaction receipt")
        return receipt

    def _save(self, journal: dict) -> None:
        self.state.write(f"{journal['plan_id']}.json", journal)

    def _outcome(self, journal: dict, status: str, files: list[Json]) -> TransactionReceipt:
        receipt: TransactionReceipt = {
            "plan_id": journal["plan_id"],
            "status": status,
            "files": files,
        }
        journal.update(status=status, receipt=receipt)
        self._save(journal)
        return receipt

    def _check_parents(self, entry: dict, parents: tuple[FileIdentity, ...]) -> None:
        if tuple(self._identity(value) for value in entry["parents"]) != parents:
            raise AdapterError("CONFLICT", "Parent directory identity changed")

    def _cleanup(self, journal: dict) -> None:
        for entry in journal["entries"]:
            try:
                path = Path.from_uri(entry["uri"])
                with self.workspace.parent_handle(path) as (parent, parents):
                    self._check_parents(entry, parents)
                    for name in (
                        entry["before_name"],
                        entry["after_name"],
                        entry["after_name"] + ".restore",
                    ):
                        with suppress(FileNotFoundError):
                            _, identity = read_at(parent, name, self.config.limits.max_file_bytes)
                            if identity.owner != os.getuid():
                                raise AdapterError("RECOVERY_REQUIRED", "Unsafe staging owner")
                            os.unlink(name, dir_fd=parent)
                    os.fsync(parent)
            except OSError, AdapterError:
                continue  # A durable outcome stands; safe private leftovers are retained.

    def _restore(self, journal: dict) -> TransactionReceipt:
        files: list[Json] = []
        failed = False
        for index, entry in enumerate(journal["entries"]):
            status = "unknown"
            try:
                path, current = self._authorize(entry["uri"])
                with self.workspace.parent_handle(path) as (parent, parents):
                    self._check_parents(entry, parents)
                    before_identity = self._identity(entry["before_identity"])
                    backup = None
                    if journal["status"] != "preparing":
                        backup, _ = read_at(
                            parent, entry["before_name"], self.config.limits.max_file_bytes
                        )
                        if digest(backup) != entry["before_hash"]:
                            raise ValueError("Corrupt recovery image")
                    if (
                        current.sha256 == entry["before_hash"]
                        and current.identity.mode == before_identity.mode
                    ):
                        status = "before"
                    elif (
                        backup is not None
                        and current.sha256 == entry["after_hash"]
                        and current.identity == self._identity(entry["after_identity"])
                    ):
                        temporary = entry["after_name"] + ".restore"
                        with suppress(FileNotFoundError):
                            read_at(parent, temporary, self.config.limits.max_file_bytes)
                            os.unlink(temporary, dir_fd=parent)
                        write_at(
                            parent, temporary, backup, before_identity.mode, before_identity.group
                        )
                        # Recheck immediately before replacement; never overwrite an external writer.
                        latest = self.workspace.read(entry["uri"])
                        if latest.sha256 != current.sha256 or latest.identity != current.identity:
                            raise ValueError("Concurrent external writer")
                        os.replace(temporary, path.name, src_dir_fd=parent, dst_dir_fd=parent)
                        os.fsync(parent)
                        restored = self.workspace.read(entry["uri"])
                        if (
                            restored.sha256 != entry["before_hash"]
                            or restored.identity.mode != before_identity.mode
                        ):
                            raise ValueError("Restoration verification failed")
                        status = "restored"
                        self._checkpoint(f"rollback:{index}")
                    else:
                        status = "external"
                        failed = True
            except OSError, ValueError, AdapterError:
                failed = True
            files.append({"uri": entry["uri"], "status": status})
        status = "recovery_required" if failed else "rolled_back"
        self.blocked |= failed
        try:
            receipt = self._outcome(journal, status, files)
        except OSError, AdapterError:
            self.blocked = True
            return {"plan_id": journal["plan_id"], "status": "recovery_required", "files": files}
        if not failed:
            self._cleanup(journal)
        return receipt

    def recover(self) -> list[TransactionReceipt]:
        """Inspect every registered transaction before permitting any new mutation."""
        receipts = []
        for plan_id in self.state.ids:
            journal = self._journal(plan_id)
            if journal["status"] in TERMINAL:
                receipt = self.receipt(plan_id)
                assert receipt is not None
                self.blocked |= journal["status"] == "recovery_required"
                if not self.blocked:
                    self._cleanup(journal)
            else:
                receipt = self._restore(journal)
            receipts.append(receipt)
        return receipts

    def _targets(self, plan: EditPlan, stack: ExitStack) -> tuple[list, list]:
        """Preflight every target and hold its anchored parent until commit finishes."""
        targets, entries = [], []
        for base, after in zip(plan.bases, plan.after, strict=True):
            path, current = self._authorize(base.uri)
            if (
                current.sha256 != base.sha256
                or current.identity != base.identity
                or current.parents != base.parents
            ):
                raise AdapterError("CONFLICT", "Source bytes, mode or object identity changed")
            if base.data == after:
                continue
            index = len(entries)
            parent, parents = stack.enter_context(self.workspace.parent_handle(path))
            if parents != base.parents or not os.access(path.parent, os.W_OK):
                raise AdapterError("CONFLICT", "Parent directory changed or is not writable")
            entry = {
                "uri": base.uri,
                "before_hash": base.sha256,
                "after_hash": digest(after),
                "before_identity": asdict(base.identity),
                "parents": [asdict(p) for p in parents],
                "before_name": f".gz-mcp-lsp-{plan.plan_id}-{index}.before",
                "after_name": f".gz-mcp-lsp-{plan.plan_id}-{index}.after",
                "after_identity": None,
            }
            entries.append(entry)
            targets.append((parent, path, base, after))
        return targets, entries

    def _stage(self, targets: list, entries: list, journal: dict) -> None:
        """Durably verify all recovery and after images before the first replacement."""
        for index, ((parent, _, base, after), entry) in enumerate(
            zip(targets, entries, strict=True)
        ):
            write_at(parent, entry["before_name"], base.data)
            self._checkpoint(f"before:{index}")
            identity = write_at(
                parent, entry["after_name"], after, base.identity.mode, base.identity.group
            )
            entry["after_identity"] = asdict(identity)
            for name, expected in (
                (entry["before_name"], entry["before_hash"]),
                (entry["after_name"], entry["after_hash"]),
            ):
                if digest(read_at(parent, name, self.config.limits.max_file_bytes)[0]) != expected:
                    raise OSError("Staging verification failed")
            os.fsync(parent)
            self._save(journal)
            self._checkpoint(f"staged:{index}")

    def apply(self, plan: EditPlan) -> TransactionReceipt:
        """A receipt is replayed, a new plan is preflighted entirely, never recomputed."""
        previous = self.receipt(plan.plan_id)
        if previous is not None:
            return previous
        if self.blocked:
            raise AdapterError("RECOVERY_REQUIRED", "Unresolved transaction blocks mutations")
        if not self.config.mutations_enabled:
            raise AdapterError("MUTATIONS_DISABLED", "Mutations disabled by operator")
        if time.monotonic() > plan.expires_at:
            raise AdapterError("PLAN_EXPIRED", "Preview has expired")
        if self.workspace.manifest() != plan.generation:
            raise AdapterError("CONFLICT", "Workspace generation changed since preview")
        with ExitStack() as stack:
            targets, entries = self._targets(plan, stack)
            journal = {
                "schema_version": 1,
                "plan_id": plan.plan_id,
                "generation": plan.generation,
                "workspace": self.config.workspace_root.as_uri(),
                "root_identity": list(self.workspace._root_identity),
                "status": "preparing",
                "entries": entries,
            }
            copies = sum(len(base.data) + len(after) for _, _, base, after in targets)
            reserve = (
                copies * 2 + len(json.dumps(journal).encode()) * 4 + (len(self.state.ids) + 1) * 150
            )
            if self.state.usage() + reserve > self.config.limits.max_state_bytes:
                raise AdapterError("LIMIT_EXCEEDED", "Recovery state capacity exhausted")
            self.state.register(plan.plan_id)
            self._checkpoint("registered")
            self._save(journal)
            self._checkpoint("journal")
            try:
                self._stage(targets, entries, journal)
                journal["status"] = "prepared"
                self._save(journal)
                self._checkpoint("prepared")
                for index, ((parent, path, base, _), entry) in enumerate(
                    zip(targets, entries, strict=True)
                ):
                    _, current = self._authorize(base.uri)
                    if (
                        current.sha256 != base.sha256
                        or current.identity != base.identity
                        or current.parents != base.parents
                    ):
                        raise AdapterError(
                            "CONFLICT", "Source changed immediately before replacement"
                        )
                    os.replace(entry["after_name"], path.name, src_dir_fd=parent, dst_dir_fd=parent)
                    os.fsync(parent)
                    self._checkpoint(f"replace:{index}")
                for entry in entries:
                    _, current = self._authorize(entry["uri"])
                    if current.sha256 != entry["after_hash"] or current.identity != self._identity(
                        entry["after_identity"]
                    ):
                        raise OSError("Postimage verification failed")
                status = (
                    "no_op"
                    if all(base.data == after for _, _, base, after in targets)
                    else "committed"
                )
                receipt = self._outcome(
                    journal,
                    status,
                    [
                        {
                            "uri": e["uri"],
                            "before_hash": e["before_hash"],
                            "after_hash": e["after_hash"],
                        }
                        for e in entries
                    ],
                )
            except OSError, AdapterError:
                return self._restore(journal)
            self._checkpoint("receipt")
            self._cleanup(journal)
            return receipt

    def close(self) -> None:
        """Release mutation authority only after the owner finishes or records recovery."""
        if self._state is not None:
            self._state.close()
            self._state = None
