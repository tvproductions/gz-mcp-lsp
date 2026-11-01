"""Official SDK composition and strict raw input validation before SDK coercion."""

import json
from collections.abc import AsyncGenerator, Awaitable
from contextlib import asynccontextmanager
from typing import Annotated

from mcp import types
from mcp.server.context import CallNext, HandlerResult, ServerRequestContext
from mcp.server.mcpserver import MCPServer

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.diagnostics import Diagnostics
from gz_mcp_lsp.documents import Documents
from gz_mcp_lsp.models import AdapterError, Json, Position, Result
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
    if operation != "hover":
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


async def _strict_arguments(ctx: ServerRequestContext, call_next: CallNext) -> HandlerResult:
    if ctx.method == "tools/call" and ctx.params is not None:
        name = ctx.params.get("name")
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
            and name in {"hover", "definition", "references"}
            and not _position_arguments(name, ctx.params.get("arguments"))
        ):
            return _error(
                name, AdapterError("INVALID_INPUT", "Invalid exact-position tool arguments")
            )
    return await call_next(ctx)


async def _run(operation: str, task: Awaitable[Result]) -> types.CallToolResult:
    try:
        return _result(await task)
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

    @asynccontextmanager
    async def lifespan(server: MCPServer) -> AsyncGenerator[dict[str, Json]]:
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

    return server
