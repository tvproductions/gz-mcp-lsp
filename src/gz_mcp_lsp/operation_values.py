"""Shared semantic capability, context and complete-response invariants."""

import json

from gz_mcp_lsp.documents import Documents
from gz_mcp_lsp.models import AdapterError, Json, Result, Snapshot
from gz_mcp_lsp.ports import SessionPort


def require_capability(session: SessionPort, name: str) -> None:
    """Distinguish unsupported operations from successful empty semantic results."""
    value = session.capabilities.get(name)
    if value is None or value is False:
        raise AdapterError("UNSUPPORTED", "Language server does not advertise this operation")


def context_limit(value: int) -> None:
    """Context has a small explicit bound, with no numeric coercion."""
    if type(value) is not int or not 0 <= value <= 20:
        raise AdapterError("INVALID_INPUT", "context_lines must be an integer from 0 to 20")


def envelope(
    operation: str, result: Json, documents: Documents, snapshots: list[Snapshot]
) -> Result:
    """Bound the complete normalized result, never silently truncate a reference set."""
    response: Result = {
        "schema_version": 1,
        "operation": operation,
        "position_encoding": "utf-16",
        "result": result,
        "workspace_generation": documents.session.generation,
        "documents": [{"uri": s.uri, "sha256": s.sha256, "version": s.version} for s in snapshots],
        "complete": True,
    }
    if (
        len(json.dumps(response, ensure_ascii=False).encode("utf-8"))
        > documents.workspace.config.limits.max_result_bytes
    ):
        raise AdapterError("RESULT_LIMIT", "Complete semantic result exceeds the configured limit")
    return response
