"""Verify installed MCP→adapter→actual ty from outside the source checkout."""

import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def main():
    """Require correct semantic content, not merely registration or a response."""
    executable, settings, uri = sys.argv[1:]
    params = StdioServerParameters(command=executable, args=["--config", settings])
    async with stdio_client(params) as (reader, writer), ClientSession(reader, writer) as client:
        await client.initialize()
        result = await client.call_tool(
            "hover", {"uri": uri, "position": {"line": 0, "character": 4}}
        )
        if result.is_error or "installed_probe" not in json.dumps(result.structured_content):
            raise ValueError(f"Installed semantic probe failed: {result.content}")
        print(
            json.dumps(
                {
                    "installed_executable": executable,
                    "settings": str(Path(settings)),
                    "operation": "hover",
                    "semantic_assertion": "installed_probe",
                    "passed": True,
                }
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
