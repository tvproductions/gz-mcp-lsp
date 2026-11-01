"""Saved-byte declaration extraction; AST byte columns never become semantic inputs."""

import ast
import io
import re
import tokenize
import unicodedata
from collections.abc import Iterator
from typing import cast

from gz_mcp_lsp.models import AdapterError, Json, Position, Range, Snapshot
from gz_mcp_lsp.workspace import Workspace


def position_json(value: Position) -> dict[str, Json]:
    """Serialize a validated coordinate without changing its meaning."""

    return {"line": value.line, "character": value.character}


def range_json(value: Range) -> dict[str, Json]:
    """Preserve both end-exclusive endpoints."""

    return {"start": position_json(value.start), "end": position_json(value.end)}


def parse_position(value: object) -> Position:
    """Validate untrusted server coordinates without Python coercion."""

    if not isinstance(value, dict) or not {"line", "character"} <= value.keys():
        raise AdapterError("PROTOCOL_ERROR", "Language server returned an invalid position")
    try:
        return Position(value["line"], value["character"])
    except AdapterError as error:
        raise AdapterError(
            "PROTOCOL_ERROR", "Language server returned invalid coordinates"
        ) from error


def parse_range(value: object) -> Range:
    """Validate an ordered server range."""

    if not isinstance(value, dict) or not {"start", "end"} <= value.keys():
        raise AdapterError("PROTOCOL_ERROR", "Language server returned an invalid range")
    try:
        return Range(parse_position(value["start"]), parse_position(value["end"]))
    except AdapterError as error:
        raise AdapterError("PROTOCOL_ERROR", "Language server returned an invalid range") from error


def _contains(extent: Range, position: Position) -> bool:
    return (
        (extent.start.line, extent.start.character)
        <= (position.line, position.character)
        < (extent.end.line, extent.end.character)
    )


def _matches(identifier: Range, requested: Range, full: Range) -> bool:
    return identifier == requested or _contains(identifier, requested.start) or full == requested


def _line_starts(snapshot: Snapshot) -> list[int]:
    return [0, *(match.end() for match in re.finditer(rb"\r\n|\r|\n", snapshot.data))]


def _ast_position(snapshot: Snapshot, line: int, byte_column: int) -> Position:
    starts = _line_starts(snapshot)
    start = starts[line - 1]
    prefix = snapshot.data[start : start + byte_column].decode("utf-8")
    return Position(line - 1, len(prefix.encode("utf-16-le")) // 2)


def _ast_range(snapshot: Snapshot, node: ast.stmt | ast.Name) -> Range:
    if node.end_lineno is None or node.end_col_offset is None:
        raise AdapterError("PROTOCOL_ERROR", "Syntax lacks complete source coordinates")
    return Range(
        _ast_position(snapshot, node.lineno, node.col_offset),
        _ast_position(snapshot, node.end_lineno, node.end_col_offset),
    )


def _name_range(
    snapshot: Snapshot, node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef
) -> Range:
    text = snapshot.data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    after_keyword = False
    for token in tokenize.generate_tokens(io.StringIO(text).readline):
        if token.start[0] != node.lineno:
            continue
        if token.string in {"def", "class"}:
            after_keyword = True
            continue
        if after_keyword and token.type == tokenize.NAME:
            if unicodedata.normalize("NFKC", token.string) != node.name:
                break
            line = text.split("\n")[token.start[0] - 1]
            start = len(line[: token.start[1]].encode("utf-16-le")) // 2
            end = len(line[: token.end[1]].encode("utf-16-le")) // 2
            return Range(Position(token.start[0] - 1, start), Position(token.end[0] - 1, end))
    raise AdapterError("PROTOCOL_ERROR", "Unable to locate declaration identifier")


def _ast_candidates(
    snapshot: Snapshot, tree: ast.AST, selection: Range
) -> Iterator[tuple[Range, Range]]:
    for node in ast.walk(tree):
        if isinstance(node, ast.stmt):
            first = node.lineno
            if (
                isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef)
                and node.decorator_list
            ):
                first = node.decorator_list[0].lineno
            if node.end_lineno is None or not first <= selection.start.line + 1 <= node.end_lineno:
                continue
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            full = _ast_range(snapshot, node)
            if node.decorator_list:
                first = node.decorator_list[0]
                full = Range(_ast_position(snapshot, first.lineno, node.col_offset), full.end)
            yield full, _name_range(snapshot, node)
        elif isinstance(node, ast.Assign | ast.AnnAssign):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                for name in ast.walk(target):
                    if isinstance(name, ast.Name):
                        yield _ast_range(snapshot, node), _ast_range(snapshot, name)


def _symbol_candidates(symbols: Json, uri: str) -> Iterator[tuple[Range, Range]]:
    if symbols is None:
        return
    if not isinstance(symbols, list):
        raise AdapterError("PROTOCOL_ERROR", "Invalid declaration symbols")
    for symbol in symbols:
        if not isinstance(symbol, dict):
            raise AdapterError("PROTOCOL_ERROR", "Invalid declaration symbol")
        if "selectionRange" in symbol:
            yield parse_range(symbol.get("range")), parse_range(symbol["selectionRange"])
            yield from _symbol_candidates(symbol.get("children"), uri)
        elif isinstance(symbol.get("location"), dict):
            # Flat SymbolInformation has no distinct identifier range.
            location = cast("dict[str, Json]", symbol["location"])
            if location.get("uri") == uri:
                extent = parse_range(location.get("range"))
                yield extent, extent


def declaration(snapshot: Snapshot, selection: Range, symbols: Json) -> dict[str, Json]:
    """Find complete matching syntax/symbol bounds; never return a query position."""

    Workspace.offset(snapshot, selection.start)
    Workspace.offset(snapshot, selection.end)
    candidates = [
        (full, identifier)
        for full, identifier in _symbol_candidates(symbols, snapshot.uri)
        if _matches(identifier, selection, full)
    ]
    syntax_incomplete = False
    try:
        tree = ast.parse(snapshot.data.decode("utf-8"))
        syntax = [
            (full, identifier)
            for full, identifier in _ast_candidates(snapshot, tree, selection)
            if _matches(identifier, selection, full)
        ]
        # AST expands decorated functions whose server full range starts at def.
        candidates = syntax or candidates
    except SyntaxError:
        syntax_incomplete = True
    except RecursionError as error:
        raise AdapterError("LIMIT_EXCEEDED", "Declaration syntax exceeds parsing depth") from error
    if not candidates:
        return {
            "text": None,
            "source_scope": "workspace",
            "source_status": "syntax_incomplete" if syntax_incomplete else "unavailable",
            "sha256": snapshot.sha256,
            "complete": False,
        }
    full, identifier = min(
        candidates,
        key=lambda item: (
            Workspace.offset(snapshot, item[0].end) - Workspace.offset(snapshot, item[0].start)
        ),
    )
    start = Workspace.offset(snapshot, full.start)
    end = Workspace.offset(snapshot, full.end)
    return {
        "text": snapshot.data[start:end].decode("utf-8"),
        "full_range": range_json(full),
        "selection_range": range_json(identifier),
        "source_scope": "workspace",
        "source_status": "syntax_incomplete" if syntax_incomplete else "complete",
        "sha256": snapshot.sha256,
        "complete": not syntax_incomplete,
    }


def source_context(snapshot: Snapshot, extent: Range, lines: int) -> dict[str, Json]:
    """Extract bounded saved lines, preserving CR/LF and byte spelling."""

    Workspace.offset(snapshot, extent.start)
    Workspace.offset(snapshot, extent.end)
    starts = _line_starts(snapshot)
    first = max(0, extent.start.line - lines)
    after = min(len(starts), extent.end.line + lines + 1)
    start = starts[first]
    end = starts[after] if after < len(starts) else len(snapshot.data)
    return {
        "text": snapshot.data[start:end].decode("utf-8"),
        "start_line": first,
        "sha256": snapshot.sha256,
        "source_scope": "workspace",
    }
