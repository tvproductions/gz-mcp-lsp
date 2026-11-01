"""Official SDK composition and strict raw input validation before SDK coercion."""

import json
from collections.abc import AsyncGenerator, Awaitable
from contextlib import asynccontextmanager
from typing import Annotated, Literal

from mcp import types
from mcp.server.context import CallNext, HandlerResult, ServerRequestContext
from mcp.server.mcpserver import MCPServer

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.diagnostics import Diagnostics
from gz_mcp_lsp.documents import Documents
from gz_mcp_lsp.filesystem import Transactions
from gz_mcp_lsp.models import AdapterError, Json, Position, Result, TextEdit
from gz_mcp_lsp.mutations import Mutations
from gz_mcp_lsp.navigation import Navigation
from gz_mcp_lsp.session import Session
from gz_mcp_lsp.workspace import Workspace


def _result(value: Result, *, error: bool = False) -> types.CallToolResult:
    return types.CallToolResult(
        is_error=error,
        structured_content=value,
        content=[types.TextContent(text=json.dumps(value, ensure_ascii=False, allow_nan=False))],
    )


def _error(operation: str, error: AdapterError) -> types.CallToolResult:
    return _result(
        {
            "schema_version": 1,
            "operation": operation,
            "error": {
                "code": error.code,
                "message": error.message,
                "retryable": error.retryable,
                "details": error.details,
            },
        },
        error=True,
    )


def _position_arguments(operation: str, value: object) -> bool:
    allowed = {"uri", "position"}
    if operation in {"definition", "references"}:
        allowed.add("context_lines")
    if operation == "references":
        allowed.add("include_declaration")
    if (
        not isinstance(value, dict)
        or not {"uri", "position"} <= value.keys()
        or not value.keys() <= allowed
    ):
        return False
    position = value["position"]
    if not (
        isinstance(value["uri"], str)
        and isinstance(position, dict)
        and set(position) == {"line", "character"}
        and all(type(item) is int and item >= 0 for item in position.values())
    ):
        return False
    lines = value.get("context_lines", 0)
    return (
        type(lines) is int
        and 0 <= lines <= 20
        and type(value.get("include_declaration", False)) is bool
    )


def _mutation_arguments(name: str, value: object) -> bool:
    if not isinstance(value, dict):
        return False
    action = value.get("action")
    if action == "apply":
        return set(value) == {"action", "plan_id"} and isinstance(value["plan_id"], str)
    if action != "preview" or not isinstance(value.get("uri"), str):
        return False
    if name == "rename_symbol":
        return (
            set(value) == {"action", "uri", "position", "new_name"}
            and isinstance(value["new_name"], str)
            and _position_arguments("hover", {"uri": value["uri"], "position": value["position"]})
        )
    if (
        set(value) != {"action", "uri", "edits", "expected_hash"}
        or not isinstance(value["expected_hash"], str)
        or not isinstance(value["edits"], list)
    ):
        return False
    for edit in value["edits"]:
        if (
            not isinstance(edit, dict)
            or set(edit) != {"range", "new_text"}
            or not isinstance(edit["new_text"], str)
        ):
            return False
        span = edit["range"]
        if not isinstance(span, dict) or set(span) != {"start", "end"}:
            return False
        if not all(
            _position_arguments("hover", {"uri": value["uri"], "position": span[key]})
            for key in ("start", "end")
        ):
            return False
    return True


async def _strict_arguments(ctx: ServerRequestContext, call_next: CallNext) -> HandlerResult:
    if ctx.method == "tools/call" and ctx.params is not None:
        name = ctx.params.get("name")
        if isinstance(name, str) and name in {"document_symbols", "workspace_symbols"}:
            arguments = ctx.params.get("arguments")
            valid = isinstance(arguments, dict)
            if valid and name == "document_symbols":
                valid = set(arguments) == {"uri"} and isinstance(arguments["uri"], str)
            elif isinstance(arguments, dict):
                valid = (
                    "query" in arguments
                    and arguments.keys() <= {"query", "resolve"}
                    and isinstance(arguments["query"], str)
                    and type(arguments.get("resolve", False)) is bool
                )
            if not valid:
                return _error(name, AdapterError("INVALID_INPUT", "Invalid symbol arguments"))
        if (
            isinstance(name, str)
            and name in {"rename_symbol", "edit_file"}
            and not _mutation_arguments(name, ctx.params.get("arguments"))
        ):
            return _error(name, AdapterError("INVALID_INPUT", "Invalid tagged mutation arguments"))
        if name == "diagnostics":
            arguments = ctx.params.get("arguments")
            if (
                not isinstance(arguments, dict)
                or "uri" not in arguments
                or not arguments.keys() <= {"uri", "context_lines"}
                or not isinstance(arguments["uri"], str)
                or type(arguments.get("context_lines", 0)) is not int
                or not 0 <= arguments.get("context_lines", 0) <= 20
            ):
                return _error(
                    "diagnostics", AdapterError("INVALID_INPUT", "Invalid diagnostic arguments")
                )
        if (
            isinstance(name, str)
            and name in {"hover", "definition", "references", "implementations"}
            and not _position_arguments(name, ctx.params.get("arguments"))
        ):
            return _error(
                name, AdapterError("INVALID_INPUT", "Invalid exact-position tool arguments")
            )
    return await call_next(ctx)


async def _run(operation: str, task: Awaitable[Result]) -> types.CallToolResult:
    try:
        value = await task
        if operation in {"rename_symbol", "edit_file"}:
            value = value | {"operation": operation}
        return _result(value)
    except AdapterError as error:
        return _error(operation, error)
    except Exception:
        return _error(operation, AdapterError("PROTOCOL_ERROR", "Semantic operation failed"))


def _read_annotations() -> types.ToolAnnotations:
    return types.ToolAnnotations(read_only_hint=True, destructive_hint=False, open_world_hint=False)


def create_server(config: Config, session: Session) -> MCPServer:
    """Bind one Documents coordinator and one owned session to the SDK lifespan."""

    documents = Documents(Workspace(config), session)
    navigation = Navigation(documents, session)
    diagnostic_service = Diagnostics(documents, session)
    transactions = Transactions(config, documents.workspace)
    mutations = Mutations(config, documents, session, transactions)

    @asynccontextmanager
    async def lifespan(server: MCPServer) -> AsyncGenerator[dict[str, Json]]:
        await mutations.start()
        await documents.start()
        async with session:
            try:
                yield {}
            finally:
                await documents.close()

    server = MCPServer(
        "gz-mcp-lsp",
        version="0.1.0",
        lifespan=lifespan,
        log_level="WARNING",
        instructions="Use exact file URIs and zero-based UTF-16 identifier positions.",
        middleware=[_strict_arguments],
    )

    @server.tool(annotations=_read_annotations(), structured_output=True)
    async def hover(
        uri: str, position: Position
    ) -> Annotated[types.CallToolResult, dict[str, Json]]:
        """Inspect original hover text at an exact saved-file position."""
        return await _run("hover", navigation.hover(uri, position))

    @server.tool(annotations=_read_annotations(), structured_output=True)
    async def definition(
        uri: str, position: Position, context_lines: int = 0
    ) -> Annotated[types.CallToolResult, dict[str, Json]]:
        """Resolve exact identifier definitions with complete authorized declaration source."""
        return await _run("definition", navigation.definition(uri, position, context_lines))

    @server.tool(annotations=_read_annotations(), structured_output=True)
    async def references(
        uri: str, position: Position, include_declaration: bool = False, context_lines: int = 0
    ) -> Annotated[types.CallToolResult, dict[str, Json]]:
        """List complete exact-position references and optional saved source context."""
        return await _run(
            "references", navigation.references(uri, position, include_declaration, context_lines)
        )

    @server.tool(annotations=_read_annotations(), structured_output=True)
    async def diagnostics(
        uri: str, context_lines: int = 0
    ) -> Annotated[types.CallToolResult, dict[str, Json]]:
        """Pull the full current diagnostics list for a saved file, with identity provenance."""
        return await _run("diagnostics", diagnostic_service.diagnostics(uri, context_lines))

    annotations = types.ToolAnnotations(
        read_only_hint=False, destructive_hint=True, open_world_hint=False
    )

    @server.tool(annotations=_read_annotations(), structured_output=True)
    async def document_symbols(uri: str) -> Annotated[types.CallToolResult, dict[str, Json]]:
        """List document symbols with hierarchy and distinct full/identifier ranges."""
        return await _run("document_symbols", navigation.document_symbols(uri))

    @server.tool(annotations=_read_annotations(), structured_output=True)
    async def workspace_symbols(
        query: str, resolve: bool = False
    ) -> Annotated[types.CallToolResult, dict[str, Json]]:
        """Discover ambiguous names; resolve URI-only symbols only when advertised."""
        return await _run("workspace_symbols", navigation.workspace_symbols(query, resolve))

    @server.tool(annotations=_read_annotations(), structured_output=True)
    async def implementations(
        uri: str, position: Position
    ) -> Annotated[types.CallToolResult, dict[str, Json]]:
        """Find ty subclass or member overrides at an exact identifier position."""
        return await _run("implementations", navigation.implementations(uri, position))

    @server.tool(annotations=annotations, structured_output=True)
    async def rename_symbol(
        action: Literal["preview", "apply"],
        uri: str | None = None,
        position: Position | None = None,
        new_name: str | None = None,
        plan_id: str | None = None,
    ) -> Annotated[types.CallToolResult, dict[str, Json]]:
        """Preview an exact-position rename or apply its retained plan under operator authority."""
        if action == "apply":
            assert plan_id is not None
            return await _run("rename_symbol", mutations.apply(plan_id))
        assert uri is not None and position is not None and new_name is not None
        return await _run("rename_symbol", mutations.preview_rename(uri, position, new_name))

    @server.tool(annotations=annotations, structured_output=True)
    async def edit_file(
        action: Literal["preview", "apply"],
        uri: str | None = None,
        edits: list[TextEdit] | None = None,
        expected_hash: str | None = None,
        plan_id: str | None = None,
    ) -> Annotated[types.CallToolResult, dict[str, Json]]:
        """Preview explicit existing-file edits with an exact base hash or apply a retained plan."""
        if action == "apply":
            assert plan_id is not None
            return await _run("edit_file", mutations.apply(plan_id))
        assert uri is not None and edits is not None and expected_hash is not None
        return await _run("edit_file", mutations.preview_edit(uri, edits, expected_hash))

    return server
