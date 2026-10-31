"""Exact-position semantic operations, independent of SDK and subprocess ownership."""

import json

from gz_mcp_lsp.documents import Documents
from gz_mcp_lsp.models import AdapterError, Json, Position, Result
from gz_mcp_lsp.operation_values import context_limit, envelope, require_capability
from gz_mcp_lsp.ports import SessionPort
from gz_mcp_lsp.protocol_values import position_json, range_json, range_value
from gz_mcp_lsp.source_text import declaration
from gz_mcp_lsp.symbol_values import symbol_items, symbol_value, symbols


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

    def _scopes(self, items: list[dict[str, Json]]) -> None:
        """Mark external/unavailable targets without reading their source contents."""
        pending = list(items)
        while pending:
            item = pending.pop()
            uri = item["uri"]
            assert isinstance(uri, str)
            try:
                self.documents.workspace.path(uri)
            except AdapterError as error:
                item["source_scope"] = (
                    "unavailable" if error.code == "SOURCE_UNAVAILABLE" else "external"
                )
            else:
                item["source_scope"] = "workspace"
            children = item.get("children", [])
            assert isinstance(children, list)
            for child in children:
                assert isinstance(child, dict)
                pending.append(child)

    async def document_symbols(self, uri: str) -> Result:
        """Return explicit document hierarchy or honest flat symbol metadata."""
        async with self.documents.query(uri) as snapshot:
            assert snapshot is not None
            require_capability(self.session, "documentSymbolProvider")
            raw = await self.session.rpc.request(
                "textDocument/documentSymbol",
                {"textDocument": {"uri": snapshot.uri}},
                timeout=self.documents.workspace.config.limits.request_seconds,
            )
            found = symbols(raw, snapshot.uri)
            self._scopes(found)
            return envelope(
                "document_symbols", {"symbols": list(found)}, self.documents, [snapshot]
            )

    async def workspace_symbols(self, query: str, resolve: bool = False) -> Result:
        """Keep ambiguous names and URI-only locations; resolve only by explicit request."""
        if not isinstance(query, str) or type(resolve) is not bool:
            raise AdapterError(
                "INVALID_INPUT", "Expected a symbol query string and Boolean resolve"
            )
        async with self.documents.query(None):
            require_capability(self.session, "workspaceSymbolProvider")
            capability = self.session.capabilities["workspaceSymbolProvider"]
            if resolve and not (
                isinstance(capability, dict) and capability.get("resolveProvider") is True
            ):
                raise AdapterError("UNSUPPORTED", "Workspace symbol resolution is unavailable")
            raw = symbol_items(
                await self.session.rpc.request(
                    "workspace/symbol",
                    {"query": query},
                    timeout=self.documents.workspace.config.limits.request_seconds,
                )
            )
            symbols(raw)  # Validate the entire result before issuing resolution requests.
            if resolve:
                raw = await self._resolve_symbols(raw)
            found = symbols(raw)
            self._scopes(found)
            return envelope("workspace_symbols", {"symbols": list(found)}, self.documents, [])

    async def _resolve_symbols(self, raw: list[Json]) -> list[Json]:
        resolved: list[Json] = []
        for item in raw:
            before = symbol_value(item, None)
            if before["resolved"]:
                resolved.append(item)
                continue
            reply = await self.session.rpc.request(
                "workspaceSymbol/resolve",
                item,
                timeout=self.documents.workspace.config.limits.request_seconds,
            )
            after = symbol_value(reply, None)
            if any(before[key] != after[key] for key in ("name", "kind", "uri")):
                raise AdapterError("PROTOCOL_ERROR", "Workspace resolution changed symbol identity")
            resolved.append(reply)
        return resolved

    async def implementations(self, uri: str, position: Position) -> Result:
        """Forward exact identifier coordinates, retaining full and selection target ranges."""
        async with self.documents.query(uri) as snapshot:
            assert snapshot is not None
            require_capability(self.session, "implementationProvider")
            self.documents.workspace.offset(snapshot, position)
            found = locations(
                await self._query("textDocument/implementation", snapshot.uri, position)
            )
            self._scopes(found)
            return envelope(
                "implementations", {"locations": list(found)}, self.documents, [snapshot]
            )

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
