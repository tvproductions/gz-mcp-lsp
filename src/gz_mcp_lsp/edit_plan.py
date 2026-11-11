"""Immutable, filesystem-free edit planning over exact saved preimages."""

import hashlib
import json
import math
import re
import stat
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from itertools import pairwise
from typing import cast
from urllib.parse import quote, unquote_to_bytes, urlsplit

from gz_mcp_lsp.config import Limits
from gz_mcp_lsp.models import AdapterError, Json, Range, Snapshot, TextEdit
from gz_mcp_lsp.results import encoded_size
from gz_mcp_lsp.source_text import parse_range, range_json
from gz_mcp_lsp.workspace import Workspace

_DEFAULT_LIMITS = Limits()


@dataclass(frozen=True, slots=True)
class ChangeAnnotation:
    """Preview-visible confirmation metadata; never evidence of human consent."""

    annotation_id: str
    label: str
    description: str | None
    needs_confirmation: bool


@dataclass(frozen=True, slots=True)
class PlannedEdit:
    """One original-snapshot range and optional bound annotation."""

    range: Range
    new_text: str
    annotation_id: str | None = None


@dataclass(frozen=True, slots=True)
class PlannedFile:
    """Exact immutable before/after bytes for one existing physical file."""

    uri: str
    before: Snapshot
    after: bytes
    edits: tuple[PlannedEdit, ...]


@dataclass(frozen=True, slots=True)
class EditPlan:
    """Content identity and expiry under one workspace/session generation."""

    plan_id: str
    generation: str
    files: tuple[PlannedFile, ...]
    expires_at: float
    annotations: tuple[ChangeAnnotation, ...]

    @property
    def no_op(self) -> bool:
        """A no-op has no differing target byte image."""

        return all(file.before.data == file.after for file in self.files)


def _verified_snapshot(snapshot: Snapshot, limits: Limits) -> None:
    if (
        not isinstance(snapshot.data, bytes)
        or hashlib.sha256(snapshot.data).hexdigest() != snapshot.sha256
    ):
        raise AdapterError("CONFLICT", "Preimage hash does not match its exact saved bytes")
    if len(snapshot.data) > limits.file_bytes:
        raise AdapterError("LIMIT_EXCEEDED", "Preimage exceeds the file byte limit")
    if type(snapshot.version) is not int or snapshot.version < 0:
        raise AdapterError("CONFLICT", "Invalid saved document version")
    try:
        snapshot.data.decode("utf-8")
    except UnicodeError as error:
        raise AdapterError("INVALID_INPUT", "Edit preimage must be UTF-8") from error


def plan_edits(
    snapshot: Snapshot, edits: Sequence[TextEdit], *, limits: Limits = _DEFAULT_LIMITS
) -> bytes:
    """Apply nonoverlapping original-byte ranges without reading or writing a path."""

    _verified_snapshot(snapshot, limits)
    if len(edits) > limits.mutation_edits:
        raise AdapterError("LIMIT_EXCEEDED", "Too many edits")
    offsets = []
    for edit in edits:
        if not isinstance(edit, TextEdit):
            raise AdapterError("INVALID_INPUT", "Expected explicit text edits")
        start = Workspace.offset(snapshot, edit.range.start)
        end = Workspace.offset(snapshot, edit.range.end)
        try:
            text = edit.new_text.encode("utf-8")
        except UnicodeError as error:
            raise AdapterError("INVALID_INPUT", "New text must be valid UTF-8") from error
        offsets.append((start, end, text))
    offsets.sort(key=lambda value: (value[0], value[1]))
    for previous, current in pairwise(offsets):
        if previous[1] > current[0] or previous[0] == previous[1] == current[0] == current[1]:
            raise AdapterError("CONFLICT", "Overlapping edits or coincident insertions")
    size = len(snapshot.data) + sum(len(text) - (end - start) for start, end, text in offsets)
    if size > limits.file_bytes or size > limits.staged_bytes:
        raise AdapterError("LIMIT_EXCEEDED", "Edited file exceeds its byte budget")
    # Assemble from original preimages once; no offset is ever adjusted by earlier edits.
    output = bytearray()
    cursor = 0
    for start, end, text in offsets:
        output.extend(snapshot.data[cursor:start])
        output.extend(text)
        cursor = end
    output.extend(snapshot.data[cursor:])
    return bytes(output)


def _uri_key(uri: str) -> str:
    if (
        not isinstance(uri, str)
        or "?" in uri
        or "#" in uri
        or re.search(r"%(?![0-9a-fA-F]{2})", uri)
    ):
        raise AdapterError("UNSUPPORTED", "Malformed mutation URI")
    try:
        parsed = urlsplit(uri)
        decoded = unquote_to_bytes(parsed.path).decode("utf-8")
    except (ValueError, UnicodeError) as error:
        raise AdapterError("UNSUPPORTED", "Malformed mutation URI") from error
    if (
        parsed.scheme != "file"
        or parsed.netloc
        or not decoded.startswith("/")
        or decoded.startswith("//")
        or "\0" in decoded
        or "\\" in decoded
        or any(part in {".", ".."} for part in decoded.split("/"))
    ):
        raise AdapterError("UNSUPPORTED", "Mutation targets require local nontraversing file URIs")
    decoded = "/".join(part for part in decoded.split("/") if part)
    return "file:///" + quote(decoded, safe="/:")


def _annotations(value: Json, limits: Limits) -> tuple[ChangeAnnotation, ...]:
    if value is None:
        return ()
    if not isinstance(value, dict) or len(value) > limits.mutation_edits:
        raise AdapterError("UNSUPPORTED", "Invalid change annotations")
    annotations = []
    for identifier, annotation in sorted(value.items()):
        if (
            not identifier
            or not isinstance(annotation, dict)
            or not {"label"} <= annotation.keys()
            or not annotation.keys() <= {"label", "description", "needsConfirmation"}
            or not isinstance(annotation["label"], str)
            or type(annotation.get("needsConfirmation", False)) is not bool
        ):
            raise AdapterError("UNSUPPORTED", "Unsupported change annotation")
        description = annotation.get("description")
        if description is not None and not isinstance(description, str):
            raise AdapterError("UNSUPPORTED", "Invalid annotation description")
        annotations.append(
            ChangeAnnotation(
                identifier,
                annotation["label"],
                description,
                cast("bool", annotation.get("needsConfirmation", False)),
            )
        )
    return tuple(annotations)


def _documents(edit: dict[str, Json]) -> list[tuple[str, int | None, list[Json]]]:
    if "changes" in edit and "documentChanges" in edit:
        raise AdapterError("UNSUPPORTED", "Contradictory WorkspaceEdit forms")
    documents = []
    if "changes" in edit:
        changes = edit["changes"]
        if not isinstance(changes, dict):
            raise AdapterError("UNSUPPORTED", "Invalid WorkspaceEdit changes")
        for uri, edits in changes.items():
            if not isinstance(edits, list):
                raise AdapterError("UNSUPPORTED", "Invalid text edit list")
            documents.append((uri, None, edits))
    elif "documentChanges" in edit:
        changes = edit["documentChanges"]
        if not isinstance(changes, list):
            raise AdapterError("UNSUPPORTED", "Invalid documentChanges")
        for change in changes:
            if (
                not isinstance(change, dict)
                or set(change) != {"textDocument", "edits"}
                or not isinstance(change["textDocument"], dict)
                or not isinstance(change["edits"], list)
            ):
                raise AdapterError("UNSUPPORTED", "Filesystem resource operations are unsupported")
            document = change["textDocument"]
            if set(document) != {"uri", "version"} or not isinstance(document["uri"], str):
                raise AdapterError("UNSUPPORTED", "Invalid versioned document identifier")
            version = document["version"]
            if version is not None and type(version) is not int:
                raise AdapterError("UNSUPPORTED", "Document version must be an integer or null")
            documents.append((document["uri"], version, change["edits"]))
    return documents


def _edits(raw: list[Json], annotations: set[str]) -> tuple[PlannedEdit, ...]:
    edits = []
    for value in raw:
        if (
            not isinstance(value, dict)
            or not {"range", "newText"} <= value.keys()
            or not value.keys() <= {"range", "newText", "annotationId"}
            or not isinstance(value["newText"], str)
        ):
            raise AdapterError("UNSUPPORTED", "Unsupported text edit shape")
        identifier = value.get("annotationId")
        if identifier is not None and (
            not isinstance(identifier, str) or identifier not in annotations
        ):
            raise AdapterError("UNSUPPORTED", "Text edit references an unknown annotation")
        edits.append(PlannedEdit(parse_range(value["range"]), value["newText"], identifier))
    return tuple(
        sorted(
            edits,
            key=lambda edit: (
                edit.range.start.line,
                edit.range.start.character,
                edit.range.end.line,
                edit.range.end.character,
            ),
        )
    )


def _input_size(edit: Json) -> int:
    try:
        return encoded_size(edit)
    except (TypeError, ValueError, UnicodeError) as error:
        raise AdapterError(
            "INVALID_INPUT", "WorkspaceEdit must contain valid UTF-8 JSON"
        ) from error


def plan_workspace_edit(
    edit: Json,
    snapshots: Mapping[str, Snapshot],
    generation: str,
    *,
    limits: Limits = _DEFAULT_LIMITS,
    expires_at: float | None = None,
) -> EditPlan:
    """Validate the entire edit and calculate bound after-images before any target IO."""

    if (
        not isinstance(edit, dict)
        or not edit.keys() <= {"changes", "documentChanges", "changeAnnotations"}
        or not isinstance(generation, str)
        or not generation
    ):
        raise AdapterError("UNSUPPORTED", "Unsupported WorkspaceEdit")
    if _input_size(edit) > limits.staged_bytes:
        raise AdapterError("LIMIT_EXCEEDED", "WorkspaceEdit metadata exceeds its byte budget")
    expiry = time.time() + limits.plan_ttl_seconds if expires_at is None else expires_at
    if type(expiry) not in (float, int) or not math.isfinite(expiry) or expiry <= 0:
        raise AdapterError("INVALID_INPUT", "Plan expiry must be finite and positive")
    annotations = _annotations(edit.get("changeAnnotations"), limits)
    documents = _documents(edit)
    if len(documents) > limits.mutation_files:
        raise AdapterError("LIMIT_EXCEEDED", "Too many mutation targets")
    files = []
    seen_uris: set[str] = set()
    seen_identities: set[tuple[int, int]] = set()
    edit_count = staged = 0
    for uri, version, raw in sorted(documents, key=lambda item: _uri_key(item[0])):
        key = _uri_key(uri)
        snapshot = snapshots.get(uri)
        if snapshot is None or _uri_key(snapshot.uri) != key:
            raise AdapterError("SOURCE_UNAVAILABLE", "A complete matching preimage is required")
        identity = snapshot.identity
        physical = identity.device, identity.inode
        if key in seen_uris or physical in seen_identities:
            raise AdapterError("CONFLICT", "Duplicate physical mutation targets or URI aliases")
        _preimage(snapshot, version)
        seen_uris.add(key)
        seen_identities.add(physical)
        edits = _edits(raw, {annotation.annotation_id for annotation in annotations})
        edit_count += len(edits)
        if edit_count > limits.mutation_edits:
            raise AdapterError("LIMIT_EXCEEDED", "Too many edits across mutation targets")
        after = plan_edits(
            snapshot, [TextEdit(item.range, item.new_text) for item in edits], limits=limits
        )
        staged += len(snapshot.data) + len(after)
        if staged > limits.staged_bytes:
            raise AdapterError(
                "LIMIT_EXCEEDED", "Before/after images exceed the staging byte budget"
            )
        files.append(PlannedFile(uri, snapshot, after, edits))
    plan = EditPlan("", generation, tuple(files), float(expiry), annotations)
    return replace(plan, plan_id=plan_digest(plan))


def _preimage(snapshot: Snapshot, version: int | None) -> None:
    """Require the exact saved version and safe physical identity for one target."""

    identity = snapshot.identity
    if not stat.S_ISREG(identity.mode) or identity.links != 1 or identity.inode == 0:
        raise AdapterError("UNSUPPORTED", "Mutation preimage lacks safe single-file identity")
    if version is not None and version != snapshot.version:
        raise AdapterError("CONFLICT", "WorkspaceEdit document version differs from preimage")


def plan_payload(plan: EditPlan) -> dict[str, Json]:
    """Private canonical metadata binds exact image hashes, edits and confirmation labels."""

    files: list[Json] = []
    for file in plan.files:
        identity = file.before.identity
        edits: list[Json] = [
            {
                "range": range_json(edit.range),
                "new_text": edit.new_text,
                "annotation_id": edit.annotation_id,
            }
            for edit in file.edits
        ]
        files.append(
            {
                "uri": file.uri,
                "snapshot_uri": file.before.uri,
                "before_hash": file.before.sha256,
                "before_image_hash": hashlib.sha256(file.before.data).hexdigest(),
                "after_hash": hashlib.sha256(file.after).hexdigest(),
                "version": file.before.version,
                "identity": {
                    "device": identity.device,
                    "inode": identity.inode,
                    "mode": identity.mode,
                    "links": identity.links,
                },
                "edits": edits,
            }
        )
    annotations: list[Json] = [
        {
            "annotation_id": item.annotation_id,
            "label": item.label,
            "description": item.description,
            "needs_confirmation": item.needs_confirmation,
        }
        for item in plan.annotations
    ]
    return {
        "schema_version": 1,
        "generation": plan.generation,
        "expires_at": plan.expires_at,
        "files": files,
        "annotations": annotations,
    }


def plan_digest(plan: EditPlan) -> str:
    """No approval flag, random token or mutable container participates in identity."""

    data = json.dumps(
        plan_payload(plan),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(data).hexdigest()
