"""Verify selected SDK behavior on the project's actual Python interpreter."""

import asyncio
import unittest
from dataclasses import dataclass

from mcp import types
from mcp.client import Client
from mcp.server.context import CallNext, HandlerResult, ServerRequestContext
from mcp.server.mcpserver import MCPServer


@dataclass
class ProbePosition:
    """Use stdlib annotations to exercise the SDK's Python 3.14 introspection."""

    line: int
    character: int


class SDKContractTests(unittest.IsolatedAsyncioTestCase):
    """Prove schemas, structured results and incoming cancellation before adapter work."""

    async def test_dataclass_schema_and_structured_result(self):
        """The selected SDK exposes coordinates and returns structured JSON."""
        server = MCPServer("sdk-contract")

        @server.tool()
        async def coordinate(position: ProbePosition) -> dict[str, int]:
            return {"line": position.line, "character": position.character}

        async with Client(server) as client:
            tools = (await client.list_tools()).tools
            self.assertEqual([tool.name for tool in tools], ["coordinate"])
            schema = tools[0].input_schema
            self.assertEqual(schema["properties"]["position"]["$ref"], "#/$defs/ProbePosition")
            self.assertEqual(schema["$defs"]["ProbePosition"]["required"], ["line", "character"])
            result = await client.call_tool("coordinate", {"position": {"line": 2, "character": 3}})
            self.assertFalse(result.is_error)
            self.assertEqual(result.structured_content, {"line": 2, "character": 3})

    async def test_raw_input_can_be_rejected_before_sdk_coercion(self):
        """Public SDK middleware can preserve strict bool-versus-int validation."""
        called = False

        async def reject_bool(ctx: ServerRequestContext, call_next: CallNext) -> HandlerResult:
            if ctx.method == "tools/call" and ctx.params is not None:
                value = ctx.params["arguments"]["position"]["line"]
                if type(value) is not int:
                    return types.CallToolResult(
                        is_error=True, content=[types.TextContent(text="INVALID_INPUT")]
                    )
            return await call_next(ctx)

        server = MCPServer("sdk-raw-input", middleware=[reject_bool])

        @server.tool()
        async def coordinate(position: ProbePosition) -> dict[str, int]:
            nonlocal called
            called = True
            return {"line": position.line}

        async with Client(server) as client:
            result = await client.call_tool(
                "coordinate", {"position": {"line": True, "character": 0}}
            )
            self.assertTrue(result.is_error)
            self.assertFalse(called)

    async def test_incoming_cancellation_releases_handler(self):
        """A cancelled client request reaches and unwinds the running SDK handler."""
        server = MCPServer("sdk-cancellation")
        started = asyncio.Event()
        finished = asyncio.Event()

        @server.tool()
        async def wait_until_cancelled() -> str:
            started.set()
            try:
                await asyncio.Event().wait()
                return "unexpected"
            finally:
                finished.set()

        async with Client(server) as client:
            task = asyncio.create_task(client.call_tool("wait_until_cancelled"))
            await asyncio.wait_for(started.wait(), 5)
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await task
            await asyncio.wait_for(finished.wait(), 5)
