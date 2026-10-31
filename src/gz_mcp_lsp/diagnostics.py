"""Current pull diagnostics; push notifications never stand in for pull results."""

import json
from collections import OrderedDict

from gz_mcp_lsp.documents import Documents
from gz_mcp_lsp.models import AdapterError, Json, Result
from gz_mcp_lsp.operation_values import context_limit, envelope, require_capability
from gz_mcp_lsp.ports import SessionPort
from gz_mcp_lsp.protocol_values import range_value


def diagnostic_items(value: Json) -> list[Json]:
    """Validate complete diagnostic items and sort by numeric range and stable content."""
    if not isinstance(value, list):
        raise AdapterError("PROTOCOL_ERROR", "Missing full diagnostic items")
    for item in value:
        if not isinstance(item, dict) or not isinstance(item.get("message"), str):
            raise AdapterError("PROTOCOL_ERROR", "Invalid diagnostic item")
        range_value(item.get("range"))
        severity = item.get("severity")
        if severity is not None and (type(severity) is not int or not 1 <= severity <= 4):
            raise AdapterError("PROTOCOL_ERROR", "Invalid diagnostic severity")
        code = item.get("code")
        if code is not None and type(code) not in (int, str):
            raise AdapterError("PROTOCOL_ERROR", "Invalid diagnostic code")

    def key(item):
        span = range_value(item["range"])
        return (
            span.start.line,
            span.start.character,
            span.end.line,
            span.end.character,
            json.dumps(item, sort_keys=True),
        )

    return sorted(value, key=key)


class Diagnostics:
    """Bound resultId cache by document and workspace generation."""

    def __init__(self, documents: Documents, session: SessionPort):
        self.documents = documents
        self.session = session
        self.cache: OrderedDict[str, tuple[str, list[Json]]] = OrderedDict()
        self.generation = ""

    def _report(self, uri: str, report: Json) -> tuple[str | None, list[Json]]:
        if not isinstance(report, dict):
            raise AdapterError("PROTOCOL_ERROR", "Invalid pull diagnostic report")
        result_id = report.get("resultId")
        if result_id is not None and not isinstance(result_id, str):
            raise AdapterError("PROTOCOL_ERROR", "Invalid diagnostic result ID")
        if report.get("kind") == "full":
            return result_id, diagnostic_items(report.get("items"))
        cached = self.cache.get(uri)
        if report.get("kind") != "unchanged" or cached is None or result_id != cached[0]:
            raise AdapterError("PROTOCOL_ERROR", "Unmatched unchanged diagnostic report")
        return cached

    def _remember(self, uri: str, result_id: str | None, items: list[Json]) -> None:
        if result_id is None:
            self.cache.pop(uri, None)
            return
        self.cache[uri] = (result_id, items)
        self.cache.move_to_end(uri)
        while len(self.cache) > 128:
            self.cache.popitem(last=False)

    async def diagnostics(self, uri: str, context_lines: int = 0) -> Result:
        """A server error or malformed report is never an empty clean result."""
        context_limit(context_lines)
        require_capability(self.session, "diagnosticProvider")
        async with self.documents.query(uri) as snapshot:
            assert snapshot is not None
            if self.generation != self.session.generation:
                self.cache.clear()
                self.generation = self.session.generation
            params: dict[str, Json] = {"textDocument": {"uri": snapshot.uri}}
            cached = self.cache.get(snapshot.uri)
            if cached is not None:
                params["previousResultId"] = cached[0]
            report = await self.session.rpc.request(
                "textDocument/diagnostic",
                params,
                timeout=self.documents.workspace.config.limits.request_seconds,
            )
            result_id, items = self._report(snapshot.uri, report)
            related = report.get("relatedDocuments", {}) if isinstance(report, dict) else {}
            if not isinstance(related, dict):
                raise AdapterError("PROTOCOL_ERROR", "Invalid related diagnostic reports")
            related_results: list[Json] = []
            pending = [(snapshot.uri, result_id, items)]
            for target, value in sorted(related.items()):
                target_id, target_items = self._report(target, value)
                status = "available"
                try:
                    self.documents.workspace.path(target)
                except AdapterError as error:
                    status = "external" if error.code == "OUTSIDE_WORKSPACE" else "unavailable"
                related_results.append(
                    {
                        "uri": target,
                        "source_status": status,
                        "items": target_items,
                        "result_id": target_id,
                    }
                )
                pending.append((target, target_id, target_items))
            # Context comes from the same saved preimage; preserve all diagnostic metadata.
            presented: list[Json] = []
            lines = snapshot.data.decode("utf-8").splitlines()
            for value in items:
                assert isinstance(value, dict)
                item = dict(value)
                if context_lines:
                    line = range_value(item["range"]).start.line
                    first, last = (
                        max(0, line - context_lines),
                        min(len(lines), line + context_lines + 1),
                    )
                    item["context"] = {"start_line": first, "text": "\n".join(lines[first:last])}
                presented.append(item)
            response = envelope(
                "diagnostics",
                {"items": presented, "result_id": result_id, "related_documents": related_results},
                self.documents,
                [snapshot],
            )
            for target, target_id, target_items in pending:
                self._remember(target, target_id, target_items)
            return response
