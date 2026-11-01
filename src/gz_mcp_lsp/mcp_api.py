"""Official SDK composition; only implemented product tools are registered."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from mcp.server.mcpserver import MCPServer

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.models import Json
from gz_mcp_lsp.session import Session


def create_server(config: Config, session: Session) -> MCPServer:
    """Bind one owned session to the SDK's stdio lifespan."""

    @asynccontextmanager
    async def lifespan(server: MCPServer) -> AsyncGenerator[dict[str, Json]]:
        async with session:
            yield {}

    return MCPServer(
        "gz-mcp-lsp",
        version="0.1.0",
        lifespan=lifespan,
        log_level="WARNING",
        instructions="Use exact file URIs and identifier positions for semantic queries.",
    )
