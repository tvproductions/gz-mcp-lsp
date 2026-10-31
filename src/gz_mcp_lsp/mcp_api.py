"""Official SDK boundary with strict inputs and equivalent JSON/text responses."""

import json
from collections.abc import Awaitable, Callable
from contextlib import asynccontextmanager, suppress
from typing import Annotated

from mcp import types
from mcp.server import MCPServer
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.diagnostics import Diagnostics
from gz_mcp_lsp.documents import Documents
from gz_mcp_lsp.models import AdapterError, Position, Result
from gz_mcp_lsp.navigation import Navigation
from gz_mcp_lsp.session import Session
from gz_mcp_lsp.workspace import Workspace

type Coordinate = Annotated[int, Field(strict=True, ge=0)]
type ContextLines = Annotated[int, Field(strict=True, ge=0, le=20)]


class InputPosition(BaseModel):
    """Strict host-facing coordinates; SDK coercion must not change semantic identity."""

    model_config = ConfigDict(extra="forbid")
    line: Coordinate
    character: Coordinate

    def domain(self) -> Position:
        """Cross into dependency-free semantic values only after validation."""
        return Position(self.line, self.character)


async def invoke(operation: str, call: Callable[[], Awaitable[Result]]) -> types.CallToolResult:
    """Keep domain errors distinct from empty successes and redact implementation traces."""
    failed = False
    try:
        result = await call()
    except AdapterError as error:
        failed = True
        result = {
            "schema_version": 1,
            "operation": operation,
            "error": {
                "code": error.code,
                "message": error.message,
                "retryable": error.retryable,
                "details": error.details,
            },
        }
    return types.CallToolResult(
        content=[types.TextContent(text=json.dumps(result, ensure_ascii=False, sort_keys=True))],
        structured_content=result,
        is_error=failed,
    )


def create_server(config: Config, session: Session) -> MCPServer:
    """Let the SDK own MCP negotiation, stdio and lifespan cancellation."""
    if config.mutations_enabled:
        raise AdapterError("UNSUPPORTED", "This read-only server does not support mutations")
    documents = Documents(Workspace(config), session)
    navigation = Navigation(documents, session)
    diagnostic_service = Diagnostics(documents, session)

    @asynccontextmanager
    async def lifespan(server: MCPServer):
        async with session:
            try:
                yield session
            finally:
                with suppress(AdapterError):
                    await documents.close()

    server = MCPServer("gz-mcp-lsp", lifespan=lifespan)
    read = types.ToolAnnotations(read_only_hint=True, destructive_hint=False, open_world_hint=False)

    @server.tool(annotations=read, structured_output=False)
    async def definition(
        uri: StrictStr, position: InputPosition, context_lines: ContextLines = 0
    ) -> types.CallToolResult:
        """Resolve an exact UTF-16 identifier position and retrieve authorized declaration source."""
        return await invoke(
            "definition", lambda: navigation.definition(uri, position.domain(), context_lines)
        )

    @server.tool(annotations=read, structured_output=False)
    async def references(
        uri: StrictStr,
        position: InputPosition,
        include_declaration: StrictBool = False,
        context_lines: ContextLines = 0,
    ) -> types.CallToolResult:
        """Find precise semantic references, retaining same-name ambiguity only in discovery tools."""
        return await invoke(
            "references",
            lambda: navigation.references(
                uri, position.domain(), include_declaration, context_lines
            ),
        )

    @server.tool(annotations=read, structured_output=False)
    async def hover(uri: StrictStr, position: InputPosition) -> types.CallToolResult:
        """Retrieve ty's semantic hover and inferred type text at an exact UTF-16 position."""
        return await invoke("hover", lambda: navigation.hover(uri, position.domain()))

    @server.tool(annotations=read, structured_output=False)
    async def diagnostics(uri: StrictStr, context_lines: ContextLines = 0) -> types.CallToolResult:
        """Return current pull diagnostics, retaining severities, codes and exact ranges."""
        return await invoke(
            "diagnostics", lambda: diagnostic_service.diagnostics(uri, context_lines)
        )

    @server.tool(annotations=read, structured_output=False)
    async def document_symbols(uri: StrictStr) -> types.CallToolResult:
        """List document symbols, preserving hierarchy and identifier selection ranges."""
        return await invoke("document_symbols", lambda: navigation.document_symbols(uri))

    @server.tool(annotations=read, structured_output=False)
    async def workspace_symbols(
        query: StrictStr, resolve: StrictBool = False
    ) -> types.CallToolResult:
        """Discover workspace symbols without choosing an ambiguous name or guessing a position."""
        return await invoke(
            "workspace_symbols", lambda: navigation.workspace_symbols(query, resolve)
        )

    @server.tool(annotations=read, structured_output=False)
    async def implementations(uri: StrictStr, position: InputPosition) -> types.CallToolResult:
        """Find known class and member implementations at an exact UTF-16 identifier position."""
        return await invoke(
            "implementations", lambda: navigation.implementations(uri, position.domain())
        )

    return server
