"""Source-free semantic envelopes and deterministic JSON byte budgets."""

import json

from gz_mcp_lsp.models import AdapterError, Json, Result, Snapshot


def encoded_size(value: object) -> int:
    """Count the complete untruncated UTF-8 JSON value."""

    return len(json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8"))


def bounded(value: object, limit: int) -> int:
    """Fail before publishing a result whose contents exceed operator authority."""

    size = encoded_size(value)
    if size > limit:
        raise AdapterError("RESULT_LIMIT", "Semantic result exceeds its byte budget")
    return size


def provenance(snapshot: Snapshot) -> Json:
    """Retain identity without retaining another copy of the saved source bytes."""

    return {"uri": snapshot.uri, "sha256": snapshot.sha256, "version": snapshot.version}


def envelope(
    operation: str, generation: str, result: Json, documents: dict[str, Json], limit: int
) -> Result:
    """Serialize one schema across independently owned semantic operations."""

    value: Result = {
        "schema_version": 1,
        "operation": operation,
        "position_encoding": "utf-16",
        "result": result,
        "workspace_generation": generation,
        "documents": [documents[uri] for uri in sorted(documents)],
        "complete": True,
    }
    bounded(value, limit)
    return value
