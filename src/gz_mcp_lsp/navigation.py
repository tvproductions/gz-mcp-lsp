"""Exact-position semantic operations over pinned saved-byte generations."""

import json
from typing import cast
from urllib.parse import urlsplit

from gz_mcp_lsp.documents import Documents, GenerationContext, _owned_io
from gz_mcp_lsp.models import AdapterError, Json, Position, Range, Result, Snapshot
from gz_mcp_lsp.session import Session
from gz_mcp_lsp.source_text import (
    declaration,
    parse_range,
    position_json,
    range_json,
    source_context,
)


class Navigation:
    """Preserve server positions and text; attach only authorized source provenance."""

    def __init__(self, documents: Documents, session: Session):
        self.documents = documents
        self.session = session

    def _require(self, provider: str) -> None:
        value = self.session.capabilities.get(provider)
        if value is not True and not isinstance(value, dict):
            raise AdapterError("UNSUPPORTED", "Language server does not advertise this operation")

    async def _request(self, context: GenerationContext, method: str, params: Json) -> Json:
        return await context.rpc.request(
            method, params, timeout=self.documents.workspace.config.request_timeout_seconds
        )

    def _bounded(self, value: object) -> None:
        size = len(json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8"))
        if size > self.documents.workspace.config.limits.result_bytes:
            raise AdapterError("RESULT_LIMIT", "Semantic result exceeds its byte budget")

    def _accumulate(self, used: int, value: Json) -> int:
        total = used + len(json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8"))
        if total > self.documents.workspace.config.limits.result_bytes:
            raise AdapterError("RESULT_LIMIT", "Source attachments exceed the result byte budget")
        return total

    def _envelope(
        self, operation: str, context: GenerationContext, result: Json, documents: dict[str, Json]
    ) -> Result:
        envelope: Result = {
            "schema_version": 1,
            "operation": operation,
            "position_encoding": "utf-16",
            "result": result,
            "workspace_generation": context.generation,
            "documents": [documents[uri] for uri in sorted(documents)],
            "complete": True,
        }
        self._bounded(envelope)
        return envelope

    async def hover(self, uri: str, position: Position) -> Result:
        """Return original legal Hover content forms or null, with saved provenance."""

        async with self.documents.read(uri) as read:
            context = GenerationContext(read.generation, read.rpc)
            self.documents.workspace.offset(read.snapshot, position)
            self._require("hoverProvider")
            result = await self._request(context, "textDocument/hover", _params(uri, position))
            _validate_hover(result)
            envelope = self._envelope("hover", context, result, {uri: _provenance(read.snapshot)})
        return envelope

    async def definition(self, uri: str, position: Position, context_lines: int = 0) -> Result:
        """Resolve exact identifier positions and attach complete authorized declarations."""

        _context_lines(context_lines)
        async with self.documents.read(uri) as read:
            context = GenerationContext(read.generation, read.rpc)
            self.documents.workspace.offset(read.snapshot, position)
            self._require("definitionProvider")
            result = await self._request(context, "textDocument/definition", _params(uri, position))
            locations = _locations(result, links=True)
            self._bounded(locations)
            documents = {uri: _provenance(read.snapshot)}
            used = 0
            for location in locations:
                snapshot = await self._source(location, context, context_lines, definition=True)
                if snapshot is not None:
                    documents[snapshot.uri] = _provenance(snapshot)
                used = self._accumulate(used, location)
            envelope = self._envelope(
                "definition", context, {"locations": cast("list[Json]", locations)}, documents
            )
        return envelope

    async def references(
        self,
        uri: str,
        position: Position,
        include_declaration: bool = False,
        context_lines: int = 0,
    ) -> Result:
        """Return deterministic complete references, with optional bounded saved context."""

        _context_lines(context_lines)
        if type(include_declaration) is not bool:
            raise AdapterError("INVALID_INPUT", "include_declaration must be boolean")
        async with self.documents.read(uri) as read:
            context = GenerationContext(read.generation, read.rpc)
            self.documents.workspace.offset(read.snapshot, position)
            self._require("referencesProvider")
            params = _params(uri, position)
            params["context"] = {"includeDeclaration": include_declaration}
            result = await self._request(context, "textDocument/references", params)
            locations = _locations(result, links=False)
            self._bounded(locations)
            documents = {uri: _provenance(read.snapshot)}
            used = 0
            for location in locations:
                if context_lines:
                    snapshot = await self._source(
                        location, context, context_lines, definition=False
                    )
                    if snapshot is not None:
                        documents[snapshot.uri] = _provenance(snapshot)
                else:
                    await self._scope(location)
                used = self._accumulate(used, location)
            envelope = self._envelope(
                "references", context, {"locations": cast("list[Json]", locations)}, documents
            )
        return envelope

    async def _scope(self, location: dict[str, Json]) -> bool:
        uri = cast("str", location["uri"])
        try:
            parsed = urlsplit(uri)
        except ValueError as error:
            raise AdapterError("PROTOCOL_ERROR", "Malformed target URI") from error
        if parsed.scheme != "file" or parsed.netloc:
            location.update(
                {"source_scope": "external", "source_status": "external", "source": None}
            )
            return False
        try:
            await _owned_io(self.documents.workspace.path, uri)
        except AdapterError as error:
            if error.code == "OUTSIDE_WORKSPACE":
                location.update(
                    {"source_scope": "external", "source_status": "external", "source": None}
                )
                return False
            if error.code in {"SOURCE_UNAVAILABLE", "INVALID_INPUT"}:
                location.update(
                    {"source_scope": "unavailable", "source_status": "unavailable", "source": None}
                )
                return False
            raise
        location["source_scope"] = "workspace"
        return True

    async def _source(
        self, location: dict[str, Json], context: GenerationContext, lines: int, *, definition: bool
    ) -> Snapshot | None:
        uri = cast("str", location["uri"])
        if not await self._scope(location):
            return None
        async with self.documents.document(context, uri) as snapshot:
            extent = parse_range(location.get("selection_range") or location["range"])
            try:
                if definition:
                    symbols = None
                    provider = self.session.capabilities.get("documentSymbolProvider")
                    if provider is True or isinstance(provider, dict):
                        symbols = await self._request(
                            context, "textDocument/documentSymbol", {"textDocument": {"uri": uri}}
                        )
                    source = await _owned_io(declaration, snapshot, extent, symbols)
                    location["source"] = source
                    location["source_scope"] = source["source_scope"]
                    location["source_status"] = source["source_status"]
                    if location.get("selection_range") is None:
                        location["selection_range"] = source.get("selection_range")
                if lines:
                    location["context"] = source_context(snapshot, extent, lines)
            except AdapterError as error:
                if error.code == "INVALID_INPUT":
                    raise AdapterError(
                        "PROTOCOL_ERROR", "Server target lies outside saved source"
                    ) from error
                raise
            return snapshot


def _provenance(snapshot: Snapshot) -> Json:
    return {"uri": snapshot.uri, "sha256": snapshot.sha256, "version": snapshot.version}


def _context_lines(value: int) -> None:
    if type(value) is not int or not 0 <= value <= 20:
        raise AdapterError(
            "INVALID_INPUT", "context_lines must be an integer from zero through twenty"
        )


def _params(uri: str, position: Position) -> dict[str, Json]:
    return {"textDocument": {"uri": uri}, "position": position_json(position)}


def _range_key(extent: Range) -> tuple[int, int, int, int]:
    return (extent.start.line, extent.start.character, extent.end.line, extent.end.character)


def _locations(result: Json, *, links: bool) -> list[dict[str, Json]]:
    if result is None:
        return []
    raw = result if isinstance(result, list) else [result]
    locations: list[dict[str, Json]] = []
    for value in raw:
        if not isinstance(value, dict):
            raise AdapterError("PROTOCOL_ERROR", "Invalid language-server location")
        if "targetUri" in value and links:
            uri = value["targetUri"]
            full = parse_range(value.get("targetRange"))
            selection = parse_range(value.get("targetSelectionRange"))
            if (
                _range_key(selection)[:2] < _range_key(full)[:2]
                or _range_key(selection)[2:] > _range_key(full)[2:]
            ):
                raise AdapterError("PROTOCOL_ERROR", "Target selection is outside its full range")
            item: dict[str, Json] = {
                "uri": uri,
                "range": range_json(full),
                "selection_range": range_json(selection),
            }
            if "originSelectionRange" in value:
                item["origin_selection_range"] = range_json(
                    parse_range(value["originSelectionRange"])
                )
        elif "uri" in value and "range" in value:
            uri = value["uri"]
            item = {
                "uri": uri,
                "range": range_json(parse_range(value["range"])),
                "selection_range": None,
            }
        else:
            raise AdapterError("PROTOCOL_ERROR", "Invalid location variant")
        if not isinstance(uri, str) or not uri:
            raise AdapterError("PROTOCOL_ERROR", "Location requires a URI")
        locations.append(item)
    return sorted(
        locations,
        key=lambda item: (
            cast("str", item["uri"]),
            _range_key(parse_range(item["range"])),
            json.dumps(item, sort_keys=True, ensure_ascii=False),
        ),
    )


def _marked(value: Json) -> bool:
    return isinstance(value, str) or (
        isinstance(value, dict)
        and isinstance(value.get("language"), str)
        and isinstance(value.get("value"), str)
    )


def _validate_hover(value: Json) -> None:
    if value is None:
        return
    if not isinstance(value, dict) or "contents" not in value:
        raise AdapterError("PROTOCOL_ERROR", "Invalid hover result")
    contents = value["contents"]
    markup = (
        isinstance(contents, dict)
        and contents.get("kind") in ("plaintext", "markdown")
        and isinstance(contents.get("value"), str)
    )
    if not (
        _marked(contents)
        or markup
        or (isinstance(contents, list) and all(_marked(v) for v in contents))
    ):
        raise AdapterError("PROTOCOL_ERROR", "Invalid hover content")
    if "range" in value:
        parse_range(value["range"])
