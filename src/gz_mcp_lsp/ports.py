"""Structural seams used by semantic tests; no server registry or framework."""

from typing import Protocol

from gz_mcp_lsp.models import Json


class RpcPort(Protocol):
    """The two LSP message operations consumed by semantic services."""

    async def request(self, method: str, params: Json, *, timeout: float) -> Json:
        """Issue one deadline-bound correlated request."""
        ...

    async def notify(self, method: str, params: Json) -> None:
        """Send a notification or perform an explicit generation transition."""
        ...


class SessionPort(Protocol):
    """Observable saved-workspace session state and explicit generation restart."""

    generation: str
    capabilities: dict[str, Json]

    @property
    def rpc(self) -> RpcPort:
        """Provide the active protocol peer."""
        ...

    async def restart(self, generation: str) -> None:
        """Send a notification or perform an explicit generation transition."""
        ...
