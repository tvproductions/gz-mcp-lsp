"""Pure bounded WorkspaceEdit validation and immutable before/after content plans."""

import hashlib
import json
import re
import time
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit

from gz_mcp_lsp.config import Limits
from gz_mcp_lsp.coordinates import byte_offset
from gz_mcp_lsp.models import AdapterError, Snapshot, TextEdit
from gz_mcp_lsp.protocol_values import range_json, range_value

DEFAULT_LIMITS = Limits()


@dataclass(frozen=True)
class EditPlan:
    """Content identity is distinct from human approval and from preview lifetime."""

    plan_id: str
    generation: str
    bases: tuple[Snapshot, ...]
    after: tuple[bytes, ...]
    edits_json: str
    annotations_json: str
    expires_at: float


def edit_uri(value: object) -> str:
    """Canonicalize URI syntax only; callers authorize every supplied snapshot."""
    if not isinstance(value, str) or re.search(r"%(?![0-9a-fA-F]{2})", value):
        raise AdapterError("INVALID_INPUT", "Invalid edit URI")
    parsed = urlsplit(value)
    try:
        path = Path(unquote(parsed.path, encoding="utf-8", errors="strict"))
    except UnicodeError as error:
        raise AdapterError("INVALID_INPUT", "Invalid edit URI encoding") from error
    if (
        parsed.scheme != "file"
        or parsed.netloc
        or parsed.query
        or parsed.fragment
        or not path.is_absolute()
        or ".." in path.parts
        or "\x00" in str(path)
    ):
        raise AdapterError("OUTSIDE_WORKSPACE", "Edit URI must identify an authorized local file")
    return path.as_uri()


def plan_edits(
    snapshot: Snapshot, edits: Sequence[TextEdit], *, max_bytes: int = DEFAULT_LIMITS.max_file_bytes
) -> bytes:
    """Apply nonoverlapping ranges to the original bytes, never shifted prior results."""
    if len(edits) > DEFAULT_LIMITS.max_edits:
        raise AdapterError("LIMIT_EXCEEDED", "Too many text edits")
    spans = []
    inserted = 0
    for edit in edits:
        if not isinstance(edit.new_text, str):
            raise AdapterError("INVALID_INPUT", "Replacement text must be a string")
        if len(edit.new_text) > max_bytes:
            raise AdapterError("LIMIT_EXCEEDED", "Replacement text exceeds file limit")
        try:
            replacement = edit.new_text.encode("utf-8")
        except UnicodeError as error:
            raise AdapterError("INVALID_INPUT", "Replacement text must be valid UTF-8") from error
        if b"\0" in replacement:
            raise AdapterError("INVALID_INPUT", "Replacement text cannot contain NUL")
        start, end = byte_offset(snapshot, edit.range.start), byte_offset(snapshot, edit.range.end)
        inserted += len(replacement)
        if inserted > max_bytes + len(snapshot.data):
            raise AdapterError("LIMIT_EXCEEDED", "Replacement allocation exceeds file limit")
        spans.append((start, end, replacement))
    spans.sort(key=lambda item: (item[0], item[1]))
    cursor = 0
    previous = None
    pieces = []
    for start, end, replacement in spans:
        if start < cursor or (previous == (start, start) and start == end):
            raise AdapterError("CONFLICT", "Edit ranges overlap or have coincident insertions")
        pieces.extend((snapshot.data[cursor:start], replacement))
        cursor = end
        previous = (start, end)
    pieces.append(snapshot.data[cursor:])
    if sum(len(piece) for piece in pieces) > max_bytes:
        raise AdapterError("LIMIT_EXCEEDED", "Edited file exceeds size limit")
    return b"".join(pieces)


def change_annotations(value: object) -> dict:
    """Validate confirmation metadata independently from the two edit-set forms."""
    annotations = value
    if not isinstance(annotations, dict):
        raise AdapterError("PROTOCOL_ERROR", "Invalid change annotations")
    for key, annotation in annotations.items():
        if (
            not isinstance(key, str)
            or not isinstance(annotation, dict)
            or set(annotation) - {"label", "needsConfirmation", "description"}
        ):
            raise AdapterError("PROTOCOL_ERROR", "Invalid change annotation")
        if (
            not isinstance(annotation.get("label"), str)
            or type(annotation.get("needsConfirmation", False)) is not bool
        ):
            raise AdapterError("PROTOCOL_ERROR", "Invalid change annotation fields")
        if "description" in annotation and not isinstance(annotation["description"], str):
            raise AdapterError("PROTOCOL_ERROR", "Invalid change annotation description")
    return annotations


def workspace_edit_sets(edit: object) -> tuple[list[tuple[str, object, object]], dict]:
    """Accept either LSP text edit form; reject resource operations and contradictions."""
    if not isinstance(edit, dict) or set(edit) - {
        "changes",
        "documentChanges",
        "changeAnnotations",
    }:
        raise AdapterError("UNSUPPORTED", "Unsupported WorkspaceEdit shape")
    if ("changes" in edit) == ("documentChanges" in edit):
        raise AdapterError("INVALID_INPUT", "WorkspaceEdit requires exactly one text edit form")
    annotations = change_annotations(edit.get("changeAnnotations", {}))
    result = []
    if "changes" in edit:
        changes = edit["changes"]
        if not isinstance(changes, dict):
            raise AdapterError("PROTOCOL_ERROR", "Invalid changes map")
        result = [(edit_uri(uri), None, edits) for uri, edits in changes.items()]
    else:
        changes = edit["documentChanges"]
        if not isinstance(changes, list):
            raise AdapterError("PROTOCOL_ERROR", "Invalid document changes")
        for item in changes:
            if not isinstance(item, dict) or set(item) != {"textDocument", "edits"}:
                raise AdapterError("UNSUPPORTED", "Filesystem resource operations are disabled")
            document = item["textDocument"]
            if not isinstance(document, dict) or set(document) != {"uri", "version"}:
                raise AdapterError("PROTOCOL_ERROR", "Invalid versioned document identifier")
            result.append((edit_uri(document["uri"]), document["version"], item["edits"]))
    return result, annotations


def normalized_edits(value: object, annotations: dict) -> tuple[list[TextEdit], list[dict]]:
    """Keep confirmation annotations in content identity while validating every edit."""
    if not isinstance(value, list):
        raise AdapterError("PROTOCOL_ERROR", "Expected text edit list")
    edits, normalized = [], []
    for item in value:
        if (
            not isinstance(item, dict)
            or set(item) - {"range", "newText", "annotationId"}
            or "newText" not in item
        ):
            raise AdapterError("PROTOCOL_ERROR", "Invalid text edit")
        span = range_value(item.get("range"))
        text = item["newText"]
        if not isinstance(text, str):
            raise AdapterError("PROTOCOL_ERROR", "Invalid replacement text")
        identity = item.get("annotationId")
        if identity is not None and (not isinstance(identity, str) or identity not in annotations):
            raise AdapterError("PROTOCOL_ERROR", "Unknown edit annotation")
        edits.append(TextEdit(span, text))
        normalized.append({"range": range_json(span), "new_text": text, "annotation_id": identity})
    return edits, normalized


def plan_workspace_edit(
    edit: object,
    snapshots: Mapping[str, Snapshot],
    generation: str,
    *,
    limits: Limits = DEFAULT_LIMITS,
) -> EditPlan:
    """Reject the entire set before returning a plan; perform no filesystem effects."""
    sets, annotations = workspace_edit_sets(edit)
    if len(sets) > limits.max_edit_files:
        raise AdapterError("LIMIT_EXCEEDED", "Too many edited files")
    available = {edit_uri(snapshot.uri): snapshot for snapshot in snapshots.values()}
    bases, after, normalized = [], [], []
    seen_uris, seen_objects = set(), set()
    count = staged = 0
    for uri, version, values in sorted(sets, key=lambda item: item[0]):
        snapshot = available.get(uri)
        if snapshot is None:
            raise AdapterError("OUTSIDE_WORKSPACE", "Edit target has no authorized snapshot")
        identity = (snapshot.identity.device, snapshot.identity.inode)
        if uri in seen_uris or identity in seen_objects:
            raise AdapterError("CONFLICT", "Duplicate or aliased edit target")
        seen_uris.add(uri)
        seen_objects.add(identity)
        if version is not None and (type(version) is not int or version != snapshot.version):
            raise AdapterError("CONFLICT", "Document version changed")
        if isinstance(values, list) and len(values) + count > limits.max_edits:
            raise AdapterError("LIMIT_EXCEEDED", "Too many text edits")
        edits, entries = normalized_edits(values, annotations)
        count += len(edits)
        if count > limits.max_edits:
            raise AdapterError("LIMIT_EXCEEDED", "Too many text edits")
        data = plan_edits(snapshot, edits, max_bytes=limits.max_file_bytes)
        staged += len(data)
        if len(data) > limits.max_file_bytes or staged > limits.max_staged_bytes:
            raise AdapterError("LIMIT_EXCEEDED", "Staged source exceeds mutation limits")
        bases.append(snapshot)
        after.append(data)
        normalized.append({"uri": uri, "version": version, "edits": entries})
    edits_json = json.dumps(normalized, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    annotations_json = json.dumps(
        annotations, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    )
    bound = {
        "generation": generation,
        "edits": edits_json,
        "annotations": annotations_json,
        "files": [
            {
                "uri": s.uri,
                "identity": asdict(s.identity),
                "parents": [asdict(parent) for parent in s.parents],
                "version": s.version,
                "before": s.sha256,
                "after": hashlib.sha256(data).hexdigest(),
            }
            for s, data in zip(bases, after, strict=True)
        ],
    }
    digest = hashlib.sha256(
        json.dumps(bound, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()
    return EditPlan(
        digest,
        generation,
        tuple(bases),
        tuple(after),
        edits_json,
        annotations_json,
        time.monotonic() + 600,
    )
