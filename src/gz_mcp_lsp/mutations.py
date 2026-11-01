"""Bounded mutation previews and coordinated, durable saved-file application."""

import asyncio
import contextlib
import difflib
import keyword
import os
import re
import time
from collections.abc import Awaitable, Sequence
from dataclasses import asdict
from typing import cast

from gz_mcp_lsp.config import Config, write_platform_supported
from gz_mcp_lsp.documents import Documents, _owned_io
from gz_mcp_lsp.edit_plan import EditPlan, _documents, plan_payload, plan_workspace_edit
from gz_mcp_lsp.filesystem import Transactions
from gz_mcp_lsp.models import AdapterError, Json, Position, Result, Snapshot, TextEdit
from gz_mcp_lsp.results import bounded, envelope, provenance
from gz_mcp_lsp.session import Session
from gz_mcp_lsp.source_text import parse_range, range_json


class Mutations:
    """Operator authority, startup admission, immutable plans and one commit owner."""

    def __init__(
        self, config: Config, documents: Documents, session: Session, transactions: Transactions
    ):
        self.config = config
        self.documents = documents
        self.session = session
        self.transactions = transactions
        self.plans: dict[str, EditPlan] = {}
        self.ready = False
        self.lockout = False

    async def start(self) -> None:
        """Finish authorized recovery before the production lifespan can yield."""
        if self.config.mutations_enabled and write_platform_supported():
            try:
                receipts = await _owned_io(self.transactions.recover)
                self.lockout = any(r.get("status") == "recovery_required" for r in receipts)
            except Exception:
                self.lockout = True
        self.ready = True

    def _check(self) -> None:
        if not self.config.mutations_enabled:
            raise AdapterError("MUTATIONS_DISABLED", "Mutation authority is disabled")
        if not write_platform_supported():
            raise AdapterError("UNSUPPORTED", "Guarded writes are unavailable on this platform")
        if not self.ready:
            raise AdapterError("WORKSPACE_BUSY", "Startup recovery has not completed", True)
        if self.lockout:
            raise AdapterError("RECOVERY_REQUIRED", "Mutations require operator recovery")
        state = self.config.state_directory
        if (
            not self.config.writable_roots
            or state is None
            or state.is_relative_to(self.config.workspace_root)
        ):
            raise AdapterError(
                "INVALID_INPUT", "Explicit roots and outside recovery storage are required"
            )

    def _snapshot(self, uri: str) -> Snapshot:
        workspace = self.documents.workspace
        path = workspace.path(uri)
        if not any(path.is_relative_to(root) for root in self.config.writable_roots):
            raise AdapterError("OUTSIDE_WORKSPACE", "Target is outside writable roots")
        info = path.parent.stat()
        if (
            not info.st_mode & 0o222
            or not info.st_mode & 0o111
            or not os.access(path.parent, os.W_OK | os.X_OK)
        ):
            raise AdapterError("CONFLICT", "Target parent is not writable/searchable")
        snapshot = workspace.read(uri)
        if snapshot.identity.links != 1:
            raise AdapterError("UNSUPPORTED", "Hard-linked mutation targets are unsupported")
        return snapshot

    def _retain(self, operation: str, plan: EditPlan) -> Result:
        now = time.time()
        self.plans = {
            key: value
            for key, value in self.plans.items()
            if value.expires_at > now and value.generation == self.session.generation
        }
        if len(self.plans) >= self.config.limits.retained_plans:
            raise AdapterError("LIMIT_EXCEEDED", "Retained preview capacity is exhausted")
        payload = plan_payload(plan)
        self._receipt_budget(plan, payload)
        files: list[Json] = []
        for file in plan.files:
            diff = "".join(
                difflib.unified_diff(
                    file.before.data.decode("utf-8").splitlines(keepends=True),
                    file.after.decode("utf-8").splitlines(keepends=True),
                    fromfile=file.uri,
                    tofile=file.uri,
                )
            )
            files.append(
                {
                    "uri": file.uri,
                    "before_hash": file.before.sha256,
                    "after_hash": next(
                        f["after_hash"]
                        for f in cast("list[dict]", payload["files"])
                        if f["uri"] == file.uri
                    ),
                    "diff": diff,
                    "edits": [cast("Json", asdict(edit)) for edit in file.edits],
                }
            )
        preview: Json = {
            "action": "preview",
            "plan_id": plan.plan_id,
            "expires_at": plan.expires_at,
            "files": files,
            "annotations": [cast("Json", asdict(a)) for a in plan.annotations],
            "no_op": plan.no_op,
        }
        result = envelope(
            operation,
            plan.generation,
            preview,
            {file.uri: provenance(file.before) for file in plan.files},
            self.config.limits.result_bytes,
        )
        self.plans[plan.plan_id] = plan
        return result

    def _receipt_budget(self, plan: EditPlan, payload: dict[str, Json]) -> None:
        # stat identities on the two supported 64-bit platforms fit these bounds.
        identity: dict[str, Json] = {key: 2**64 for key in ("device", "inode", "mode", "links")}
        files: list[Json] = []
        for file in cast("list[dict[str, Json]]", payload["files"]):
            files.append(
                {
                    "uri": file["uri"],
                    "before_hash": file["before_hash"],
                    "after_hash": file["after_hash"],
                    "mode": 0o7777,
                    "status": "restore_intent",
                    "before_identity": identity,
                    "after_identity": identity,
                    "restore_identity": identity,
                }
            )
        receipt: dict[str, Json] = {
            "schema_version": 1,
            "plan_id": plan.plan_id,
            "workspace_root": str(self.config.workspace_root),
            "status": "recovery_required",
            "files": files,
        }
        bounded(
            self._outcome(receipt, "unavailable") | {"operation": "rename_symbol"},
            self.config.limits.result_bytes,
        )

    async def preview_edit(self, uri: str, edits: Sequence[TextEdit], expected_hash: str) -> Result:
        self._check()
        if (
            not isinstance(expected_hash, str)
            or re.fullmatch("[0-9a-f]{64}", expected_hash) is None
        ):
            raise AdapterError("INVALID_INPUT", "An exact saved-file hash is required")
        if len(edits) > self.config.limits.mutation_edits or any(
            not isinstance(e, TextEdit) for e in edits
        ):
            raise AdapterError("INVALID_INPUT", "Explicit bounded text edits are required")
        async with self.documents.generation() as context:
            snapshot = await _owned_io(self._snapshot, uri)
            if snapshot.sha256 != expected_hash:
                raise AdapterError("CONFLICT", "Expected hash differs from saved source")
            changes: dict[str, Json] = {
                uri: [{"range": range_json(e.range), "newText": e.new_text} for e in edits]
            }
            plan = plan_workspace_edit(
                {"changes": changes}, {uri: snapshot}, context.generation, limits=self.config.limits
            )
        return self._retain("edit_file", plan)

    async def preview_rename(self, uri: str, position: Position, new_name: str) -> Result:
        self._check()
        if (
            not isinstance(new_name, str)
            or not new_name.isidentifier()
            or keyword.iskeyword(new_name)
        ):
            raise AdapterError(
                "INVALID_INPUT", "New name must be a Python identifier, not a keyword"
            )
        provider = self.session.capabilities.get("renameProvider")
        if provider is not True and not isinstance(provider, dict):
            raise AdapterError("UNSUPPORTED", "Language server does not advertise rename")
        async with (
            self.documents.generation() as context,
            self.documents.document(context, uri) as origin,
        ):
            self.documents.workspace.offset(origin, position)
            params: dict[str, Json] = {
                "textDocument": {"uri": origin.uri},
                "position": asdict(position),
            }
            if isinstance(provider, dict) and provider.get("prepareProvider") is True:
                prepared = await context.rpc.request(
                    "textDocument/prepareRename",
                    params,
                    timeout=self.config.request_timeout_seconds,
                )
                if prepared is None:
                    raise AdapterError("INVALID_INPUT", "The selected position cannot be renamed")
                if not isinstance(prepared, dict):
                    raise AdapterError("PROTOCOL_ERROR", "Invalid prepareRename response")
                if prepared.get("defaultBehavior") is not True:
                    selected = parse_range(prepared.get("range", prepared))
                    self.documents.workspace.offset(origin, selected.start)
                    self.documents.workspace.offset(origin, selected.end)
            edit = await context.rpc.request(
                "textDocument/rename",
                params | {"newName": new_name},
                timeout=self.config.request_timeout_seconds,
            )
            if edit is None:
                raise AdapterError("INVALID_INPUT", "Language server returned no rename edit")
            if not isinstance(edit, dict):
                raise AdapterError("PROTOCOL_ERROR", "Invalid rename WorkspaceEdit")
            bounded(edit, self.config.limits.staged_bytes)
            targets = _documents(edit)
            if len(targets) > self.config.limits.mutation_files:
                raise AdapterError("LIMIT_EXCEEDED", "Too many rename targets")
            snapshots = {}
            for target, _, _ in targets:
                snapshots[target] = await _owned_io(self._snapshot, target)
            plan = plan_workspace_edit(
                edit, snapshots, context.generation, limits=self.config.limits
            )
        return self._retain("rename_symbol", plan)

    async def apply(self, plan_id: str) -> Result:
        self._check()
        if not isinstance(plan_id, str) or re.fullmatch("[0-9a-f]{64}", plan_id) is None:
            raise AdapterError("INVALID_INPUT", "Invalid preview identity")
        return await self._apply(plan_id)

    async def _apply(self, plan_id: str) -> Result:
        receipt = await _owned_io(self.transactions.receipt, plan_id)
        if receipt is not None:
            return self._outcome(receipt, "unchanged")
        plan = self.plans.get(plan_id)
        if plan is None or plan.expires_at <= time.time():
            self.plans.pop(plan_id, None)
            raise AdapterError(
                "PLAN_EXPIRED", "Preview is missing or expired; request a fresh preview"
            )
        async with self.documents.exclusive():
            # Another apply may have finished while this caller waited for admission.
            self._check()
            receipt = await _owned_io(self.transactions.receipt, plan_id)
            if receipt is not None:
                return self._outcome(receipt, "unchanged")
            await self.documents.validate_generation(plan.generation)
            return await _finish(self._commit(plan))

    async def _commit(self, plan: EditPlan) -> Result:
        try:
            receipt = await _owned_io(self.transactions.apply, plan)
        except AdapterError as error:
            if error.code == "RECOVERY_REQUIRED":
                self.lockout = True
                await self.documents.committed(())
            raise
        self.lockout = receipt["status"] == "recovery_required"
        semantic = "invalidated"
        try:
            snapshots = []
            if receipt["status"] == "committed":
                for file in plan.files:
                    snapshots.append(await _owned_io(self.documents.workspace.read, file.uri))
            await self.documents.committed(snapshots)
        except Exception:
            semantic = "unavailable"
            # Even a snapshot read failure must invalidate the pre-commit transport.
            with contextlib.suppress(Exception):
                await self.documents.committed(())
        self.plans.pop(plan.plan_id, None)
        return self._outcome(receipt, semantic)

    def _outcome(self, receipt: dict[str, Json], semantic: str) -> Result:
        value = envelope(
            "apply", self.session.generation, receipt, {}, self.config.limits.result_bytes
        )
        value.update({"action": "apply", "semantic_state": semantic})
        bounded(value | {"operation": "rename_symbol"}, self.config.limits.result_bytes)
        return value


async def _finish[T](operation: Awaitable[T]) -> T:
    """Retain admission through disk outcome and invalidation despite caller cancellation."""
    task = asyncio.ensure_future(operation)
    cancelled = False
    while not task.done():
        try:
            await asyncio.shield(task)
        except asyncio.CancelledError:
            cancelled = True
        except Exception:
            if not cancelled:
                raise
            break
    if cancelled:
        # Observe failures; a cancellation response must not imply zero writes.
        with contextlib.suppress(Exception):
            task.result()
        raise asyncio.CancelledError
    return task.result()
