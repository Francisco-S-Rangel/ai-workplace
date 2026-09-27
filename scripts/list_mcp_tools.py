# scripts/list_mcp_tools.py — WHY: the concrete answer to "how do you retrieve the full list of
# capabilities of an MCP server?" (topic 6). It launches the server over stdio exactly like
# Claude Code does, performs the MCP handshake, and calls `list_tools()` / `list_resources()`,
# which send the protocol requests `tools/list` and `resources/list`.
# Usage: .venv\Scripts\python.exe scripts/list_mcp_tools.py [--call "query"]
"""List (and optionally call) the tools of the study-notes MCP server via the SDK client."""

import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

ROOT = Path(__file__).resolve().parent.parent


async def main() -> None:
    params = StdioServerParameters(
        command=sys.executable, args=["-m", "mcp_server.server"], cwd=str(ROOT)
    )
    async with stdio_client(params) as (read, write), ClientSession(read, write) as session:
        init = await session.initialize()
        print(f"Server: {init.serverInfo.name} (protocol {init.protocolVersion})\n")

        tools = await session.list_tools()  # -> tools/list
        print(f"Tools ({len(tools.tools)}):")
        for tool in tools.tools:
            args = ", ".join(tool.inputSchema.get("properties", {}))
            print(f"  - {tool.name}({args}): {(tool.description or '').splitlines()[0]}")

        resources = await session.list_resources()  # -> resources/list
        print(f"\nResources ({len(resources.resources)}):")
        for res in resources.resources:
            print(f"  - {res.uri}")

        if "--call" in sys.argv:
            query = sys.argv[sys.argv.index("--call") + 1]
            result = await session.call_tool("search_notes", {"query": query, "top_k": 2})
            print(f"\nsearch_notes({query!r}):")
            for block in result.content:
                print(json.dumps(json.loads(block.text), indent=2)[:600])


if __name__ == "__main__":
    asyncio.run(main())
