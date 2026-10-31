"""Official SDK composition; tool registrations follow their implemented operations."""

from contextlib import asynccontextmanager

from mcp.server import MCPServer

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.session import Session


def create_server(config: Config, session: Session) -> MCPServer:
    """Let the SDK own MCP negotiation and stdio lifespan cancellation."""

    @asynccontextmanager
    async def lifespan(server: MCPServer):
        async with session:
            yield session

    return MCPServer("gz-mcp-lsp", lifespan=lifespan)
