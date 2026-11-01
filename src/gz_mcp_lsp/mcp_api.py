"""Official SDK composition and strict raw input validation before SDK coercion."""

import asyncio
import json
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

from mcp import types
from mcp.server.context import CallNext, HandlerResult, ServerRequestContext
from mcp.server.mcpserver import MCPServer

from gz_mcp_lsp.config import Config
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


def _hover_arguments(value: object) -> bool:
    if not isinstance(value, dict) or set(value) != {"uri", "position"}:
        return False
    position = value["position"]
    return (
        isinstance(value["uri"], str)
        and isinstance(position, dict)
        and set(position) == {"line", "character"}
        and all(type(item) is int and item >= 0 for item in position.values())
    )


async def _strict_arguments(ctx: ServerRequestContext, call_next: CallNext) -> HandlerResult:
    if (
        ctx.method == "tools/call"
        and ctx.params is not None
        and ctx.params.get("name") == "hover"
        and not _hover_arguments(ctx.params.get("arguments"))
    ):
        return _error(
            "hover",
            AdapterError("INVALID_INPUT", "Hover requires an exact URI and integer position"),
        )
    return await call_next(ctx)


def create_server(config: Config, session: Session) -> MCPServer:
    """Bind one Documents coordinator and one owned session to the SDK lifespan."""

    documents = Documents(Workspace(config), session)
    navigation = Navigation(documents, session)

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

    @server.tool(
        annotations=types.ToolAnnotations(
            read_only_hint=True,
            destructive_hint=False,
            open_world_hint=False,
        ),
        structured_output=True,
    )
    async def hover(
        uri: str, position: Position
    ) -> Annotated[types.CallToolResult, dict[str, Json]]:
        """Inspect the server's original hover text at an exact saved-file position."""
        try:
            return _result(await navigation.hover(uri, position))
        except AdapterError as error:
            return _error("hover", error)
        except asyncio.CancelledError:
            raise

    return server
