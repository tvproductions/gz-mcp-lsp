"""Python declaration presentation only; extracted positions never drive navigation."""

import ast

from gz_mcp_lsp.coordinates import byte_offset
from gz_mcp_lsp.models import Json, Position, Range, Snapshot
from gz_mcp_lsp.protocol_values import range_json, range_value


def ast_position(lines: list[bytes], line: int, byte_column: int) -> Position:
    """Convert AST's UTF-8 byte column independently of LSP's UTF-16 units."""
    prefix = lines[line][:byte_column].decode("utf-8")
    return Position(line, len(prefix.encode("utf-16-le")) // 2)


def symbol_declaration(
    snapshot: Snapshot, selection: Range, symbols: Json
) -> dict[str, Json] | None:
    """Use a server full range only when its identifier selection contains the target."""
    pending = list(symbols) if isinstance(symbols, list) else []
    while pending:
        item = pending.pop()
        if not isinstance(item, dict):
            continue
        children = item.get("children")
        if isinstance(children, list):
            pending.extend(children)
        if "selectionRange" not in item or "range" not in item:
            continue
        selected = range_value(item["selectionRange"])
        if selected.start <= selection.start and selection.end <= selected.end:
            full = range_value(item["range"])
            start, end = byte_offset(snapshot, full.start), byte_offset(snapshot, full.end)
            return {
                "source_status": "complete",
                "source_scope": "server_declaration",
                "source": snapshot.data[start:end].decode("utf-8"),
                "range": range_json(full),
                "selection_range": range_json(selected),
                "sha256": snapshot.sha256,
            }
    return None


def declaration(snapshot: Snapshot, selection: Range, symbols: Json) -> dict[str, Json]:
    """Extract the smallest containing Python declaration including its decorators."""
    server_source = symbol_declaration(snapshot, selection, symbols)
    try:
        tree = ast.parse(snapshot.data)
        lines = snapshot.data.split(b"\n")
        candidates = []
        for node in ast.walk(tree):
            if not isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Assign, ast.AnnAssign),
            ):
                continue
            assert node.end_lineno is not None and node.end_col_offset is not None
            start = ast_position(lines, node.lineno - 1, node.col_offset)
            end = ast_position(lines, node.end_lineno - 1, node.end_col_offset)
            if start <= selection.start and selection.end <= end:
                candidates.append((node, start, end))
        if not candidates:
            return server_source or {"source_status": "unavailable", "source_scope": "unknown"}
        node, start, end = min(
            candidates,
            key=lambda item: (item[2].line - item[1].line, item[2].character - item[1].character),
        )
        first_line = node.lineno - 1
        first_column = node.col_offset
        decorators = getattr(node, "decorator_list", [])
        if decorators:
            first_line = min(decorator.lineno for decorator in decorators) - 1
            first_column = 0
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            first_column = (
                0  # Include indentation for an independently complete nested source block.
            )
        start = ast_position(lines, first_line, first_column)
        begin = sum(len(line) + 1 for line in lines[:first_line]) + first_column
        assert node.end_lineno is not None and node.end_col_offset is not None
        finish = sum(len(line) + 1 for line in lines[: node.end_lineno - 1]) + node.end_col_offset
        return {
            "source_status": "complete",
            "source_scope": "declaration",
            "source": snapshot.data[begin:finish].decode("utf-8"),
            "range": range_json(Range(start, end)),
            "selection_range": range_json(selection),
            "sha256": snapshot.sha256,
        }
    except SyntaxError, ValueError, RecursionError, UnicodeError:
        return server_source or {"source_status": "unavailable", "source_scope": "unknown"}
