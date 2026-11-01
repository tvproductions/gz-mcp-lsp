"""Semantic operations over exact positions and pinned saved-file generations."""

import json

from gz_mcp_lsp.documents import Documents
from gz_mcp_lsp.models import AdapterError, Position, Result
from gz_mcp_lsp.session import Session


class Navigation:
    """Preserve server text and coordinates without guessing inferred type structures."""

    def __init__(self, documents: Documents, session: Session):
        self.documents = documents
        self.session = session

    async def hover(self, uri: str, position: Position) -> Result:
        """Return original LSP Hover content or null, with saved-byte provenance."""

        async with self.documents.read(uri) as context:
            self.documents.workspace.offset(context.snapshot, position)
            if not self.session.capabilities.get("hoverProvider"):
                raise AdapterError("UNSUPPORTED", "Language server does not advertise hover")
            result = await context.rpc.request(
                "textDocument/hover",
                {
                    "textDocument": {"uri": uri},
                    "position": {"line": position.line, "character": position.character},
                },
                timeout=self.documents.workspace.config.request_timeout_seconds,
            )
            if result is not None and (not isinstance(result, dict) or "contents" not in result):
                raise AdapterError("PROTOCOL_ERROR", "Invalid language-server hover result")
            envelope: Result = {
                "schema_version": 1,
                "operation": "hover",
                "position_encoding": "utf-16",
                "result": result,
                "workspace_generation": context.generation,
                "documents": [
                    {
                        "uri": uri,
                        "sha256": context.snapshot.sha256,
                        "version": context.snapshot.version,
                    }
                ],
                "complete": True,
            }
            size = len(json.dumps(envelope, ensure_ascii=False, allow_nan=False).encode("utf-8"))
            if size > self.documents.workspace.config.limits.result_bytes:
                raise AdapterError("RESULT_LIMIT", "Semantic result exceeds its byte budget")
        return envelope
