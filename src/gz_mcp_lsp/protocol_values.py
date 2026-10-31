"""Validate untrusted LSP values and preserve coordinate distinctions."""

from gz_mcp_lsp.models import AdapterError, Json, Position, Range


def position_value(value: Json) -> Position:
    """Parse a protocol position without coercion or inferred offsets."""
    if not isinstance(value, dict) or set(value) != {"line", "character"}:
        raise AdapterError("PROTOCOL_ERROR", "Invalid LSP position")
    line, character = value["line"], value["character"]
    if type(line) is not int or type(character) is not int or line < 0 or character < 0:
        raise AdapterError("PROTOCOL_ERROR", "Invalid LSP coordinates")
    return Position(line, character)


def range_value(value: Json) -> Range:
    """Require an ordered end-exclusive protocol range."""
    if not isinstance(value, dict) or set(value) != {"start", "end"}:
        raise AdapterError("PROTOCOL_ERROR", "Invalid LSP range")
    start, end = position_value(value["start"]), position_value(value["end"])
    if end < start:
        raise AdapterError("PROTOCOL_ERROR", "Invalid reversed LSP range")
    return Range(start, end)


def position_json(position: Position) -> dict[str, Json]:
    """Serialize one already validated domain position."""
    return {"line": position.line, "character": position.character}


def range_json(value: Range) -> dict[str, Json]:
    """Serialize one already validated domain range."""
    return {"start": position_json(value.start), "end": position_json(value.end)}
