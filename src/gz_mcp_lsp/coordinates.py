"""Pure exact-byte coordinate conversion shared by reads and edit planning."""

import re

from gz_mcp_lsp.models import AdapterError, Position, Snapshot


def line_records(data: bytes) -> list[tuple[int, bytes]]:
    """Use precisely LSP's CRLF, LF and CR delimiters, preserving saved byte starts."""
    result = []
    start = 0
    for match in re.finditer(rb"\r\n|\r|\n", data):
        result.append((start, data[start : match.start()]))
        start = match.end()
    result.append((start, data[start:]))
    return result


def byte_offset(snapshot: Snapshot, position: Position) -> int:
    """Map a valid UTF-16 position to exact UTF-8 bytes, excluding newline bytes."""
    lines = line_records(snapshot.data)
    if position.line >= len(lines):
        raise AdapterError("INVALID_INPUT", "Line is outside the document")
    offset, line = lines[position.line]
    units = 0
    for character in line.decode("utf-8"):
        if units == position.character:
            return offset
        units += 2 if ord(character) > 0xFFFF else 1
        offset += len(character.encode("utf-8"))
    if units == position.character:
        return offset
    raise AdapterError("INVALID_INPUT", "Character is outside the line or splits a surrogate pair")
