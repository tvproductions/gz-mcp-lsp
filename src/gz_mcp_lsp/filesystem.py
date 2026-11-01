"""Guarded local POSIX transactions, durable receipts and conservative recovery.

This adapter has no SDK/LSP dependency and makes no cross-file atomicity promise.
"""

import json
import os
import re
import stat
import time
from collections.abc import Generator, Sequence
from contextlib import ExitStack, contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

from gz_mcp_lsp import _posix_files as posix
from gz_mcp_lsp.config import Config
from gz_mcp_lsp.edit_plan import EditPlan, _uri_key, plan_digest, plan_payload
from gz_mcp_lsp.models import AdapterError, FileIdentity, TransactionReceipt
from gz_mcp_lsp.workspace import Workspace

_ID = re.compile(r"[0-9a-f]{64}")
_IMAGE = re.compile(r"[0-9]{4}\.(before|after)")
_PHASES = {"prepared", "applying", "rolling_back", "committed", "rolled_back", "recovery_required"}
_TERMINAL = {"committed", "no_op", "rolled_back", "recovery_required"}


@dataclass(slots=True)
class _Target:
    index: int
    path: Path
    parent: int
    parent_info: os.stat_result


def _json(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


def _unique(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("Duplicate state key")
        value[key] = item
    return value


def _bad_constant(value: str):
    raise ValueError("Nonfinite state number")


class Transactions:
    """One private state lock owns staging, commit/rollback and startup recovery."""

    def __init__(self, config: Config, workspace: Workspace):
        self.config = config
        self.workspace = workspace

    def _authority(self) -> None:
        if not self.config.mutations_enabled:
            raise AdapterError("MUTATIONS_DISABLED", "Mutation authority is disabled")
        posix.require_platform()
        root = self.workspace.root
        state = self.config.state_directory
        if (
            self.config.workspace_root != root
            or not root.is_absolute()
            or not self.config.writable_roots
            or state is None
            or not state.is_absolute()
            or state.is_relative_to(root)
        ):
            raise AdapterError(
                "INVALID_INPUT", "Explicit bounded roots and outside recovery state are required"
            )
        for writable in self.config.writable_roots:
            if not writable.is_relative_to(root) or self.workspace._excluded(
                writable.relative_to(root)
            ):
                raise AdapterError(
                    "OUTSIDE_WORKSPACE", "Writable root is outside authorized source"
                )
            with posix.opened_directory(writable):
                pass

    @contextmanager
    def _state(self) -> Generator[int]:
        self._authority()
        state = self.config.state_directory
        assert state is not None
        try:
            with posix.opened_directory(self.workspace.root) as root:
                posix.local_filesystem(root)
                device = os.fstat(root).st_dev
            with posix.opened_directory(state.parent) as parent:
                if os.fstat(parent).st_dev != device:
                    raise AdapterError(
                        "UNSUPPORTED", "Recovery state must share the source filesystem"
                    )
                try:
                    os.mkdir(state.name, 0o700, dir_fd=parent)
                    posix.sync(parent, is_directory=True)
                except FileExistsError:
                    pass
            with posix.opened_directory(state) as descriptor:
                posix.private_directory(descriptor)
                posix.local_filesystem(descriptor)
                flags = (
                    os.O_RDWR
                    | os.O_CREAT
                    | getattr(os, "O_NOFOLLOW", 0)
                    | getattr(os, "O_NONBLOCK", 0)
                )
                lock = os.open("lock", flags, 0o600, dir_fd=descriptor)
                try:
                    info = os.fstat(lock)
                    if (
                        not stat.S_ISREG(info.st_mode)
                        or info.st_nlink != 1
                        or info.st_uid != posix.uid()
                        or info.st_mode & 0o077
                    ):
                        raise AdapterError("RECOVERY_REQUIRED", "Unsafe private state lock")
                    with posix.locked(lock):
                        yield descriptor
                finally:
                    os.close(lock)
        except AdapterError:
            raise
        except OSError as error:
            raise AdapterError(
                "RECOVERY_REQUIRED", "Unable to establish safe recovery storage"
            ) from error

    def _path(self, uri: str, *, writable: bool = True) -> Path:
        path = Path(unquote(urlsplit(_uri_key(uri)).path))
        root = self.workspace.root
        if not path.is_relative_to(root) or self.workspace._excluded(path.relative_to(root)):
            raise AdapterError("OUTSIDE_WORKSPACE", "Mutation target is outside allowed source")
        if writable and not any(path.is_relative_to(root) for root in self.config.writable_roots):
            raise AdapterError("OUTSIDE_WORKSPACE", "Mutation target is outside writable roots")
        return path

    def _target(self, index: int, uri: str, stack: ExitStack) -> _Target:
        path = self._path(uri)
        descriptor = stack.enter_context(posix.opened_directory(path.parent))
        info = os.fstat(descriptor)
        if not info.st_mode & 0o222 or not info.st_mode & 0o111:
            raise AdapterError("CONFLICT", "Target parent is not writable/searchable")
        if not os.access(".", os.W_OK | os.X_OK, dir_fd=descriptor):
            raise AdapterError("CONFLICT", "Target parent access is unavailable")
        return _Target(index, path, descriptor, info)

    def _current(self, target: _Target) -> tuple[bytes, os.stat_result]:
        with posix.opened_directory(target.path.parent) as current:
            if not posix.same_directory(os.fstat(current), target.parent_info):
                raise AdapterError("CONFLICT", "Target parent changed identity")
        if not os.fstat(target.parent).st_mode & 0o222:
            raise AdapterError("CONFLICT", "Target parent permissions changed")
        return posix.read_file(target.parent, target.path.name, self.config.limits.file_bytes)

    def _state_current(self, state: int, transaction: int, plan_id: str) -> None:
        assert self.config.state_directory is not None
        with posix.opened_directory(self.config.state_directory) as current:
            posix.private_directory(current)
            if not posix.same_directory(os.fstat(current), os.fstat(state)):
                raise AdapterError("RECOVERY_REQUIRED", "Recovery directory changed identity")
        info = os.stat(plan_id, dir_fd=state, follow_symlinks=False)
        if not posix.same_directory(info, os.fstat(transaction)):
            raise AdapterError("RECOVERY_REQUIRED", "Transaction directory changed identity")

    def _usage(self, descriptor: int, depth: int = 0, deadline: float | None = None) -> int:
        if deadline is None:
            deadline = time.monotonic() + self.config.request_timeout_seconds
        total = 0
        for name in os.listdir(descriptor):
            if time.monotonic() > deadline:
                raise AdapterError("WORKSPACE_BUSY", "Recovery quota scan exceeded its budget")
            info = os.stat(name, dir_fd=descriptor, follow_symlinks=False)
            if stat.S_ISDIR(info.st_mode) and depth == 0 and _ID.fullmatch(name):
                child = os.open(
                    name,
                    os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
                    dir_fd=descriptor,
                )
                try:
                    posix.private_directory(child)
                    total += self._usage(child, 1, deadline)
                finally:
                    os.close(child)
            elif stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_uid == posix.uid():
                allowed = (
                    name in {"lock", "blocked.json", ".blocked.json.tmp"}
                    if depth == 0
                    else name
                    in {"journal.json", "receipt.json", ".journal.json.tmp", ".receipt.json.tmp"}
                    or bool(_IMAGE.fullmatch(name))
                )
                if not allowed:
                    raise AdapterError("RECOVERY_REQUIRED", "Unexpected recovery entry")
                total += info.st_size
            else:
                raise AdapterError("RECOVERY_REQUIRED", "Unsafe recovery entry")
        return total

    def _reserve(self, state: int, additional: int) -> None:
        if self._usage(state) + additional > self.config.limits.retained_state_bytes:
            raise AdapterError("LIMIT_EXCEEDED", "Private recovery state quota is exhausted")

    def _atomic_json(self, descriptor: int, name: str, record: dict) -> None:
        body = _json(record)
        data = _json({"record": record, "sha256": posix.digest(body)})
        temporary = "." + name + ".tmp"
        try:
            posix.read_file(descriptor, temporary, self._metadata_limit, private=True)
        except FileNotFoundError:
            pass
        else:
            os.unlink(temporary, dir_fd=descriptor)
        posix.write_file(descriptor, temporary, data)
        os.replace(temporary, name, src_dir_fd=descriptor, dst_dir_fd=descriptor)
        posix.sync(descriptor, is_directory=True)

    @property
    def _metadata_limit(self) -> int:
        return self.config.limits.staged_bytes * 2 + self.config.limits.result_bytes * 2 + 65536

    def _read_json(self, descriptor: int, name: str) -> dict[str, Any] | None:
        try:
            data, _ = posix.read_file(descriptor, name, self._metadata_limit, private=True)
        except FileNotFoundError:
            return None
        try:
            value = json.loads(
                data.decode("utf-8"), object_pairs_hook=_unique, parse_constant=_bad_constant
            )
            if (
                not isinstance(value, dict)
                or set(value) != {"record", "sha256"}
                or not isinstance(value["record"], dict)
                or posix.digest(_json(value["record"])) != value["sha256"]
            ):
                raise ValueError("State envelope is invalid")
            return value["record"]
        except (ValueError, UnicodeError, TypeError, RecursionError) as error:
            raise AdapterError("RECOVERY_REQUIRED", "Corrupt recovery metadata") from error

    def _transaction(self, state: int, plan_id: str, *, create: bool = False) -> int:
        if not _ID.fullmatch(plan_id):
            raise AdapterError("INVALID_INPUT", "Invalid transaction identity")
        if create:
            os.mkdir(plan_id, 0o700, dir_fd=state)
            posix.sync(state, is_directory=True)
        descriptor = os.open(
            plan_id,
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=state,
        )
        try:
            posix.private_directory(descriptor)
        except BaseException:
            os.close(descriptor)
            raise
        return descriptor

    def _write_journal(self, descriptor: int, record: dict) -> None:
        self._atomic_json(descriptor, "journal.json", record)

    def _write_receipt(self, descriptor: int, receipt: dict) -> None:
        self._atomic_json(descriptor, "receipt.json", receipt)

    def _receipt(self, descriptor: int, plan_id: str) -> dict | None:
        value = self._read_json(descriptor, "receipt.json")
        if value is not None:
            if (
                value.get("schema_version") != 1
                or value.get("plan_id") != plan_id
                or value.get("workspace_root") != str(self.workspace.root)
                or not isinstance(value.get("status"), str)
                or value["status"] not in _TERMINAL
                or not isinstance(value.get("files"), list)
                or len(value["files"]) > self.config.limits.mutation_files
            ):
                raise AdapterError("RECOVERY_REQUIRED", "Invalid durable receipt")
            for file in value["files"]:
                _validate_receipt_file(file)
                self._path(file["uri"], writable=False)
        return value

    def receipt(self, plan_id: str) -> TransactionReceipt | None:
        if not isinstance(plan_id, str) or not _ID.fullmatch(plan_id):
            raise AdapterError("INVALID_INPUT", "Invalid transaction identity")
        with self._state() as state:
            try:
                descriptor = self._transaction(state, plan_id)
            except FileNotFoundError:
                return None
            try:
                return self._receipt(descriptor, plan_id)
            finally:
                os.close(descriptor)

    def _clean(self, state: int) -> None:
        if self._read_json(state, "blocked.json") is not None:
            raise AdapterError(
                "RECOVERY_REQUIRED", "Mutations are locked pending operator recovery"
            )
        self._usage(state)
        for name in os.listdir(state):
            if not _ID.fullmatch(name):
                continue
            descriptor = self._transaction(state, name)
            try:
                self._record(descriptor, name)
                value = self._receipt(descriptor, name)
                if value is None or value["status"] == "recovery_required":
                    raise AdapterError(
                        "RECOVERY_REQUIRED", "Startup recovery is required before new mutations"
                    )
            finally:
                os.close(descriptor)

    def _record(self, descriptor: int, plan_id: str) -> dict:
        value = self._read_json(descriptor, "journal.json")
        if (
            value is None
            or value.get("schema_version") != 1
            or value.get("plan_id") != plan_id
            or value.get("workspace_root") != str(self.workspace.root)
            or not isinstance(value.get("phase"), str)
            or value["phase"] not in _PHASES
            or not isinstance(value.get("plan"), dict)
            or posix.digest(_json(value["plan"])) != plan_id
            or not isinstance(value.get("files"), list)
            or len(value["files"]) > self.config.limits.mutation_files
        ):
            raise AdapterError("RECOVERY_REQUIRED", "Invalid transaction journal")
        root_identity = value.get("workspace_identity")
        if (
            not isinstance(root_identity, list)
            or len(root_identity) != 2
            or any(type(n) is not int for n in root_identity)
        ):
            raise AdapterError("RECOVERY_REQUIRED", "Invalid saved workspace identity")
        planned = value["plan"].get("files")
        if not isinstance(planned, list) or len(planned) != len(value["files"]):
            raise AdapterError("RECOVERY_REQUIRED", "Journal target set is inconsistent")
        for file, original in zip(value["files"], planned, strict=True):
            if (
                not isinstance(file, dict)
                or not isinstance(original, dict)
                or file.get("uri") != original.get("uri")
                or file.get("before_hash") != original.get("before_hash")
                or file.get("before_hash") != original.get("before_image_hash")
                or file.get("after_hash") != original.get("after_hash")
                or file.get("before_identity") != original.get("identity")
            ):
                raise AdapterError("RECOVERY_REQUIRED", "Journal images are not bound to the plan")
            _validate_receipt_file(file, journal=True)
            for key in ("before_identity", "after_identity"):
                _validate_identity(file.get(key))
            if file.get("restore_identity") is not None:
                _validate_identity(file["restore_identity"])
            self._path(file["uri"], writable=False)
        return value

    def _prepared(
        self, state: int, transaction: int, plan: EditPlan, targets: list[_Target]
    ) -> dict:
        files = []
        for target, file in zip(targets, plan.files, strict=True):
            index = f"{target.index:04}"
            posix.write_file(transaction, index + ".before", file.before.data)
            after = posix.write_file(
                transaction, index + ".after", file.after, stat.S_IMODE(file.before.identity.mode)
            )
            before_data, _ = posix.read_file(
                transaction, index + ".before", self.config.limits.file_bytes, private=True
            )
            after_data, _ = posix.read_file(
                transaction, index + ".after", self.config.limits.file_bytes, private=True
            )
            if before_data != file.before.data or after_data != file.after:
                raise AdapterError(
                    "RECOVERY_REQUIRED", "Staged images failed exact-byte verification"
                )
            files.append(
                {
                    "uri": file.uri,
                    "before_hash": file.before.sha256,
                    "after_hash": posix.digest(file.after),
                    "before_identity": {
                        "device": file.before.identity.device,
                        "inode": file.before.identity.inode,
                        "mode": file.before.identity.mode,
                        "links": file.before.identity.links,
                    },
                    "after_identity": posix.identity(after),
                    "restore_identity": None,
                    "status": "prepared",
                }
            )
        with posix.opened_directory(self.workspace.root) as root:
            root_info = os.fstat(root)
        record = {
            "schema_version": 1,
            "plan_id": plan.plan_id,
            "workspace_root": str(self.workspace.root),
            "workspace_identity": [root_info.st_dev, root_info.st_ino],
            "plan": plan_payload(plan),
            "phase": "prepared",
            "files": files,
        }
        self._write_journal(transaction, record)
        return record

    def _replace(self, source: int, name: str, target: _Target) -> None:
        os.replace(name, target.path.name, src_dir_fd=source, dst_dir_fd=target.parent)
        posix.sync(target.parent, is_directory=True)
        posix.sync(source, is_directory=True)

    def _matches(self, target: _Target, expected: dict, sha256: str) -> bool:
        data, info = self._current(target)
        return posix.identity(info) == expected and posix.digest(data) == sha256

    def _commit(self, state: int, transaction: int, record: dict, targets: list[_Target]) -> dict:
        record["phase"] = "applying"
        for target, file in zip(targets, record["files"], strict=True):
            self._state_current(state, transaction, record["plan_id"])
            if not self._matches(target, file["before_identity"], file["before_hash"]):
                raise AdapterError("CONFLICT", "Source preimage changed before replacement")
            if file["before_hash"] == file["after_hash"]:
                file["status"] = "unchanged"
                continue
            staged, info = posix.read_file(
                transaction, f"{target.index:04}.after", self.config.limits.file_bytes, private=True
            )
            if (
                posix.identity(info) != file["after_identity"]
                or posix.digest(staged) != file["after_hash"]
            ):
                raise AdapterError("RECOVERY_REQUIRED", "Verified staging image changed")
            file["status"] = "replace_intent"
            self._write_journal(transaction, record)
            if not self._matches(target, file["before_identity"], file["before_hash"]):
                raise AdapterError("CONFLICT", "Source changed after replacement intent")
            self._replace(transaction, f"{target.index:04}.after", target)
            file["status"] = "replaced"
            self._write_journal(transaction, record)
        for target, file in zip(targets, record["files"], strict=True):
            expected = (
                file["before_identity"] if file["status"] == "unchanged" else file["after_identity"]
            )
            if not self._matches(target, expected, file["after_hash"]):
                raise AdapterError("CONFLICT", "Source postimage verification failed")
        record["phase"] = "committed"
        self._write_journal(transaction, record)
        result = self._result(
            record,
            "no_op"
            if all(f["before_hash"] == f["after_hash"] for f in record["files"])
            else "committed",
        )
        self._write_receipt(transaction, result)
        return result

    def _result(self, record: dict, status: str) -> dict:
        files = [
            {
                "uri": f["uri"],
                "before_hash": f["before_hash"],
                "after_hash": f["after_hash"],
                "mode": stat.S_IMODE(f["before_identity"]["mode"]),
                "before_identity": f["before_identity"],
                "after_identity": f["after_identity"],
                "restore_identity": f["restore_identity"],
                "status": ("unchanged" if f["before_hash"] == f["after_hash"] else "committed")
                if status in {"committed", "no_op"}
                else f["status"],
            }
            for f in record["files"]
        ]
        return {
            "schema_version": 1,
            "plan_id": record["plan_id"],
            "workspace_root": str(self.workspace.root),
            "status": status,
            "files": files,
        }

    def _restore(
        self, state: int, transaction: int, record: dict, target: _Target, file: dict
    ) -> None:
        self._state_current(state, transaction, record["plan_id"])
        data, info = self._current(target)
        current = posix.identity(info)
        digest = posix.digest(data)
        if current == file["before_identity"] and digest == file["before_hash"]:
            file["status"] = "not_written"
            return
        if current == file["restore_identity"] and digest == file["before_hash"]:
            file["status"] = "restored"
            return
        if current != file["after_identity"] or digest != file["after_hash"]:
            file["status"] = "conflict"
            return
        name = f"{target.index:04}.before"
        before, _ = posix.read_file(transaction, name, self.config.limits.file_bytes, private=True)
        if posix.digest(before) != file["before_hash"]:
            raise AdapterError("RECOVERY_REQUIRED", "Recovery preimage failed verification")
        descriptor = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=transaction)
        try:
            os.fchmod(descriptor, stat.S_IMODE(file["before_identity"]["mode"]))
            posix.sync(descriptor)
            file["restore_identity"] = posix.identity(os.fstat(descriptor))
        finally:
            os.close(descriptor)
        file["status"] = "restore_intent"
        self._write_journal(transaction, record)
        if not self._matches(target, file["after_identity"], file["after_hash"]):
            file["status"] = "conflict"
            return
        self._replace(transaction, name, target)
        if not self._matches(target, file["restore_identity"], file["before_hash"]):
            file["status"] = "conflict"
            return
        file["status"] = "restored"
        self._write_journal(transaction, record)

    def _rollback(
        self, state: int, transaction: int, record: dict, targets: Sequence[_Target | None]
    ) -> dict:
        record["phase"] = "rolling_back"
        self._write_journal(transaction, record)
        for target, file in zip(targets, record["files"], strict=True):
            try:
                if target is None:
                    raise OSError("Unavailable target parent")
                self._restore(state, transaction, record, target, file)
            except OSError, AdapterError:
                file["status"] = "unavailable"
        clean = all(f["status"] in {"not_written", "restored"} for f in record["files"])
        record["phase"] = "rolled_back" if clean else "recovery_required"
        self._write_journal(transaction, record)
        result = self._result(record, record["phase"])
        self._write_receipt(transaction, result)
        if not clean:
            self._block(state, record["plan_id"])
        return result

    def _block(self, state: int, plan_id: str) -> dict:
        result = {
            "schema_version": 1,
            "plan_id": plan_id,
            "workspace_root": str(self.workspace.root),
            "status": "recovery_required",
            "files": [],
        }
        self._atomic_json(state, "blocked.json", result)
        return result

    def apply(self, plan: EditPlan) -> TransactionReceipt:
        with self._state() as state, ExitStack() as stack:
            if not _ID.fullmatch(plan.plan_id):
                raise AdapterError("INVALID_INPUT", "Invalid plan identity")
            try:
                previous = self._transaction(state, plan.plan_id)
            except FileNotFoundError:
                previous = None
            if previous is not None:
                try:
                    result = self._receipt(previous, plan.plan_id)
                    if result is not None:
                        return result
                finally:
                    os.close(previous)
            self._clean(state)
            if plan.expires_at <= time.time():
                raise AdapterError("PLAN_EXPIRED", "Mutation preview has expired")
            if plan_digest(plan) != plan.plan_id:
                raise AdapterError("CONFLICT", "Mutation content differs from its preview identity")
            if len(plan.files) > self.config.limits.mutation_files:
                raise AdapterError("LIMIT_EXCEEDED", "Too many mutation targets")
            targets = [self._target(i, file.uri, stack) for i, file in enumerate(plan.files)]
            for target, file in zip(targets, plan.files, strict=True):
                data, info = self._current(target)
                if (
                    FileIdentity.from_stat(info) != file.before.identity
                    or data != file.before.data
                    or posix.digest(data) != file.before.sha256
                ):
                    raise AdapterError("CONFLICT", "Mutation preimage no longer matches")
                if info.st_dev != os.fstat(state).st_dev:
                    raise AdapterError(
                        "UNSUPPORTED", "Target and recovery state use different filesystems"
                    )
            size = sum(len(file.before.data) + len(file.after) for file in plan.files)
            if size > self.config.limits.staged_bytes:
                raise AdapterError("LIMIT_EXCEEDED", "Mutation images exceed staging authority")
            self._reserve(state, size * 2 + len(_json(plan_payload(plan))) * 8 + 262144)
            transaction = self._transaction(state, plan.plan_id, create=True)
            try:
                record = self._prepared(state, transaction, plan, targets)
                try:
                    return self._commit(state, transaction, record, targets)
                except OSError, AdapterError:
                    if record["phase"] == "committed":
                        raise AdapterError(
                            "RECOVERY_REQUIRED", "Commit is durable but its receipt needs recovery"
                        ) from None
                    return self._rollback(state, transaction, record, targets)
            finally:
                os.close(transaction)

    def _recover_one(self, state: int, transaction: int, record: dict) -> dict:
        previous = self._receipt(transaction, record["plan_id"])
        if previous is not None:
            return previous
        if record["phase"] == "committed":
            status = (
                "no_op"
                if all(f["before_hash"] == f["after_hash"] for f in record["files"])
                else "committed"
            )
            result = self._result(record, status)
            self._write_receipt(transaction, result)
            return result
        for file in record["files"]:
            self._path(file["uri"])
        with posix.opened_directory(self.workspace.root) as root:
            info = os.fstat(root)
        if record.get("workspace_identity") != [info.st_dev, info.st_ino]:
            raise AdapterError("RECOVERY_REQUIRED", "Recovery workspace identity changed")
        self._reserve(state, len(_json(record)) * 3 + 16384)
        with ExitStack() as stack:
            targets = []
            for index, file in enumerate(record["files"]):
                try:
                    targets.append(self._target(index, file["uri"], stack))
                except AdapterError, OSError:
                    targets.append(None)
            return self._rollback(state, transaction, record, targets)

    def recover(self) -> list[TransactionReceipt]:
        with self._state() as state:
            blocked = self._read_json(state, "blocked.json")
            if blocked is not None:
                if (
                    blocked.get("schema_version") != 1
                    or blocked.get("workspace_root") != str(self.workspace.root)
                    or blocked.get("status") != "recovery_required"
                    or not isinstance(blocked.get("plan_id"), str)
                    or (blocked["plan_id"] != "unknown" and not _ID.fullmatch(blocked["plan_id"]))
                    or blocked.get("files") != []
                ):
                    raise AdapterError("RECOVERY_REQUIRED", "Corrupt mutation lockout metadata")
                return [blocked]
            try:
                self._usage(state)
            except AdapterError, OSError:
                return [self._block(state, "unknown")]
            results = []
            for name in sorted(os.listdir(state)):
                if not _ID.fullmatch(name):
                    continue
                try:
                    descriptor = self._transaction(state, name)
                    try:
                        record = self._record(descriptor, name)
                        results.append(self._recover_one(state, descriptor, record))
                    finally:
                        os.close(descriptor)
                except AdapterError, OSError, ValueError, TypeError, KeyError:
                    results.append(self._block(state, name))
                    break
            return results


def _validate_receipt_file(file: Any, *, journal: bool = False) -> None:
    allowed = {
        "prepared",
        "unchanged",
        "replace_intent",
        "replaced",
        "restore_intent",
        "restored",
        "not_written",
        "conflict",
        "unavailable",
    }
    if not journal:
        allowed |= {"committed"}
    if (
        not isinstance(file, dict)
        or not isinstance(file.get("uri"), str)
        or not isinstance(file.get("status"), str)
        or file["status"] not in allowed
        or any(
            not isinstance(file.get(key), str) or not _ID.fullmatch(file[key])
            for key in ("before_hash", "after_hash")
        )
    ):
        raise AdapterError("RECOVERY_REQUIRED", "Invalid saved per-file outcome")
    for key in ("before_identity", "after_identity"):
        _validate_identity(file.get(key))
    if file.get("restore_identity") is not None:
        _validate_identity(file["restore_identity"])
    if not journal and (
        type(file.get("mode")) is not int
        or file["mode"] != stat.S_IMODE(file["before_identity"]["mode"])
    ):
        raise AdapterError("RECOVERY_REQUIRED", "Invalid saved file mode")


def _validate_identity(value: object) -> None:
    if (
        not isinstance(value, dict)
        or set(value) != {"device", "inode", "mode", "links"}
        or any(type(item) is not int for item in value.values())
        or value["inode"] <= 0
        or value["links"] != 1
        or not stat.S_ISREG(value["mode"])
    ):
        raise AdapterError("RECOVERY_REQUIRED", "Invalid saved file identity")
