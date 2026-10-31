"""Exact-position semantic operations, independent of SDK and subprocess ownership."""

import json

from gz_mcp_lsp.documents import Documents
from gz_mcp_lsp.models import AdapterError, Json, Position, Result, Snapshot
from gz_mcp_lsp.ports import SessionPort
from gz_mcp_lsp.protocol_values import position_json, range_json, range_value
from gz_mcp_lsp.source_text import declaration


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


def locations(value: Json) -> list[dict[str, Json]]:
    """Normalize Location and LocationLink while preserving their different ranges."""
    if value is None:
        return []
    values = value if isinstance(value, list) else [value]
    result: list[dict[str, Json]] = []
    for item in values:
        if not isinstance(item, dict):
            raise AdapterError("PROTOCOL_ERROR", "Invalid LSP location")
        linked = "targetUri" in item
        uri = item.get("targetUri" if linked else "uri")
        if not isinstance(uri, str):
            raise AdapterError("PROTOCOL_ERROR", "Missing LSP target URI")
        target_range = range_json(range_value(item.get("targetRange" if linked else "range")))
        selection = range_json(range_value(item.get("targetSelectionRange"))) if linked else None
        origin = item.get("originSelectionRange")
        result.append(
            {
                "uri": uri,
                "range": target_range,
                "selection_range": selection,
                "origin_selection_range": range_json(range_value(origin))
                if origin is not None
                else None,
            }
        )

    def key(item):
        value = range_value(item["range"])
        return (
            item["uri"],
            value.start.line,
            value.start.character,
            value.end.line,
            value.end.character,
            json.dumps(item, sort_keys=True),
        )

    result.sort(key=key)
    return result


class Navigation:
    """One operation lease surrounds all protocol work and source presentation."""

    def __init__(self, documents: Documents, session: SessionPort):
        self.documents = documents
        self.session = session

    async def _query(
        self, method: str, uri: str, position: Position, extra: dict[str, Json] | None = None
    ) -> Json:
        params: dict[str, Json] = {
            "textDocument": {"uri": uri},
            "position": position_json(position),
        }
        params.update(extra or {})
        return await self.session.rpc.request(
            method, params, timeout=self.documents.workspace.config.limits.request_seconds
        )

    def _context(self, location: dict[str, Json], count: int) -> None:
        if not count:
            return
        uri = location["uri"]
        assert isinstance(uri, str)
        try:
            snapshot = self.documents.workspace.read(uri)
        except AdapterError as error:
            location["context_status"] = (
                "external" if error.code == "OUTSIDE_WORKSPACE" else "unavailable"
            )
            return
        line = range_value(location["range"]).start.line
        lines = snapshot.data.decode("utf-8").splitlines()
        first, last = max(0, line - count), min(len(lines), line + count + 1)
        location["context"] = {
            "start_line": first,
            "text": "\n".join(lines[first:last]),
            "sha256": snapshot.sha256,
        }

    async def references(
        self,
        uri: str,
        position: Position,
        include_declaration: bool = False,
        context_lines: int = 0,
    ) -> Result:
        """Send the caller's identifier position unchanged; no symbol-name lookup."""
        context_limit(context_lines)
        if type(include_declaration) is not bool:
            raise AdapterError("INVALID_INPUT", "include_declaration must be Boolean")
        require_capability(self.session, "referencesProvider")
        async with self.documents.query(uri) as snapshot:
            assert snapshot is not None
            self.documents.workspace.offset(snapshot, position)
            found = locations(
                await self._query(
                    "textDocument/references",
                    snapshot.uri,
                    position,
                    {"context": {"includeDeclaration": include_declaration}},
                )
            )
            for item in found:
                self._context(item, context_lines)
            return envelope(
                "references", {"locations": [item for item in found]}, self.documents, [snapshot]
            )

    async def hover(self, uri: str, position: Position) -> Result:
        """Retain ty's content kind and type text without inventing a type model."""
        require_capability(self.session, "hoverProvider")
        async with self.documents.query(uri) as snapshot:
            assert snapshot is not None
            self.documents.workspace.offset(snapshot, position)
            result = await self._query("textDocument/hover", snapshot.uri, position)
            if result is not None and not isinstance(result, dict):
                raise AdapterError("PROTOCOL_ERROR", "Invalid LSP hover result")
            return envelope("hover", {"hover": result}, self.documents, [snapshot])

    async def definition(self, uri: str, position: Position, context_lines: int = 0) -> Result:
        """Retain source parity in addition to precise LSP definition navigation."""
        context_limit(context_lines)
        require_capability(self.session, "definitionProvider")
        async with self.documents.query(uri) as snapshot:
            assert snapshot is not None
            self.documents.workspace.offset(snapshot, position)
            found = locations(await self._query("textDocument/definition", snapshot.uri, position))
            for item in found:
                target_uri = item["uri"]
                assert isinstance(target_uri, str)
                try:
                    target = self.documents.workspace.read(target_uri)
                except AdapterError as error:
                    item["declaration"] = {
                        "source_status": "external"
                        if error.code == "OUTSIDE_WORKSPACE"
                        else "unavailable"
                    }
                else:
                    selected = range_value(item["selection_range"] or item["range"])
                    symbols = None
                    capability = self.session.capabilities.get("documentSymbolProvider")
                    if capability is not None and capability is not False:
                        symbols = await self.session.rpc.request(
                            "textDocument/documentSymbol",
                            {"textDocument": {"uri": target.uri}},
                            timeout=self.documents.workspace.config.limits.request_seconds,
                        )
                    item["declaration"] = declaration(target, selected, symbols)
                self._context(item, context_lines)
            return envelope(
                "definition", {"locations": [item for item in found]}, self.documents, [snapshot]
            )
