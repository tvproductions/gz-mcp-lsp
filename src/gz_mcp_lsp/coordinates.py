"""Pure exact-byte coordinate conversion shared by reads and edit planning."""

from gz_mcp_lsp.models import AdapterError, Position, Snapshot


def byte_offset(snapshot: Snapshot, position: Position) -> int:
    """Map a valid UTF-16 position to exact UTF-8 bytes, excluding newline bytes."""
    lines = snapshot.data.split(b"\n")
    if position.line >= len(lines):
        raise AdapterError("INVALID_INPUT", "Line is outside the document")
    line = lines[position.line]
    if line.endswith(b"\r"):
        line = line[:-1]
    units = 0
    offset = sum(len(value) + 1 for value in lines[: position.line])
    for character in line.decode("utf-8"):
        if units == position.character:
            return offset
        units += 2 if ord(character) > 0xFFFF else 1
        offset += len(character.encode("utf-8"))
    if units == position.character:
        return offset
    raise AdapterError("INVALID_INPUT", "Character is outside the line or splits a surrogate pair")
