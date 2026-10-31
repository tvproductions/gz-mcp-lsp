"""Normalize symbol metadata without turning full declaration ranges into identifiers."""

from gz_mcp_lsp.models import AdapterError, Json, Range
from gz_mcp_lsp.protocol_values import range_json, range_value


def symbol_items(value: Json) -> list[Json]:
    """Null means no symbols; other non-list responses are protocol failures."""
    if value is None:
        return []
    if not isinstance(value, list):
        raise AdapterError("PROTOCOL_ERROR", "Invalid LSP symbol list")
    return value


def symbol_metadata(value: Json) -> dict[str, Json]:
    """Preserve typed presentation fields, including unfamiliar positive kinds/tags."""
    if not isinstance(value, dict):
        raise AdapterError("PROTOCOL_ERROR", "Invalid LSP symbol")
    name, kind = value.get("name"), value.get("kind")
    if not isinstance(name, str) or not name.strip() or type(kind) is not int or kind < 1:
        raise AdapterError("PROTOCOL_ERROR", "Invalid symbol name or kind")
    tags, deprecated = value.get("tags", []), value.get("deprecated", False)
    if not isinstance(tags, list) or any(type(tag) is not int or tag < 1 for tag in tags):
        raise AdapterError("PROTOCOL_ERROR", "Invalid symbol tags")
    if type(deprecated) is not bool:
        raise AdapterError("PROTOCOL_ERROR", "Invalid symbol deprecation flag")
    result: dict[str, Json] = {"name": name, "kind": kind, "tags": tags, "deprecated": deprecated}
    for source, target in (("detail", "detail"), ("containerName", "container_name")):
        item = value.get(source)
        if item is not None and not isinstance(item, str):
            raise AdapterError("PROTOCOL_ERROR", "Invalid symbol presentation metadata")
        result[target] = item
    return result


def symbol_value(value: Json, uri: str | None) -> dict[str, Json]:
    """Only DocumentSymbol has a real selectionRange; flat/workspace ranges stay full."""
    result = symbol_metadata(value)
    assert isinstance(value, dict)
    selected = None
    if "location" in value:
        location = value["location"]
        if not isinstance(location, dict) or not isinstance(location.get("uri"), str):
            raise AdapterError("PROTOCOL_ERROR", "Invalid symbol location")
        target = location["uri"]
        full = range_value(location["range"]) if "range" in location else None
        if uri is not None and full is None:
            raise AdapterError("PROTOCOL_ERROR", "Flat document symbol has no range")
    else:
        if uri is None:
            raise AdapterError("PROTOCOL_ERROR", "Workspace symbol has no location")
        target = uri
        full, selected = range_value(value.get("range")), range_value(value.get("selectionRange"))
        if not full.start <= selected.start <= selected.end <= full.end:
            raise AdapterError("PROTOCOL_ERROR", "Symbol selection is outside its full range")
    if not target:
        raise AdapterError("PROTOCOL_ERROR", "Symbol URI is empty")
    result.update(
        uri=target,
        range=range_json(full) if full is not None else None,
        selection_range=range_json(selected) if selected is not None else None,
        resolved=full is not None,
        children=[],
    )
    return result


def symbol_key(item: dict[str, Json]) -> tuple:
    """Sort coordinates numerically, retaining duplicate symbol names and locations."""
    full = range_value(item["range"]) if item["range"] is not None else None
    tags = item["tags"]
    assert isinstance(tags, list)
    return (
        item["uri"],
        (full.start.line, full.start.character, full.end.line, full.end.character)
        if full is not None
        else (-1, -1, -1, -1),
        item["name"],
        item["kind"],
        item["container_name"] or "",
        item["detail"] or "",
        item["deprecated"],
        tuple(tags),
    )


def symbols(value: Json, uri: str | None = None) -> list[dict[str, Json]]:
    """Preserve explicit hierarchy iteratively; never infer hierarchy from flat metadata."""
    result: list[dict[str, Json]] = []
    pending: list[tuple[list[Json], list, Range | None]] = [(symbol_items(value), result, None)]
    while pending:
        items, destination, parent = pending.pop()
        for raw in items:
            item = symbol_value(raw, uri)
            assert isinstance(raw, dict)
            full = range_value(item["range"]) if item["range"] is not None else None
            if parent is not None and (
                "location" in raw
                or full is None
                or not parent.start <= full.start <= full.end <= parent.end
            ):
                raise AdapterError("PROTOCOL_ERROR", "Invalid nested symbol range")
            children = raw.get("children", [])
            if not isinstance(children, list) or (children and (uri is None or "location" in raw)):
                raise AdapterError("PROTOCOL_ERROR", "Invalid symbol children")
            destination.append(item)
            if children:
                normalized_children = item["children"]
                assert isinstance(normalized_children, list)
                pending.append((children, normalized_children, full))
        destination.sort(key=symbol_key)
    return result
