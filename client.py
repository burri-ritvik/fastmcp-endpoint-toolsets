"""Smoke client: prove each endpoint exposes a different tool surface."""

from __future__ import annotations

import argparse
import asyncio

from fastmcp import Client

ENDPOINTS = ["/mcp", "/json/mcp", "/text/mcp", "/math/mcp", "/time/mcp"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="List tools visible from every MCP endpoint.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8001")
    return parser.parse_args()


async def list_tools(base_url: str, path: str) -> tuple[str, list[str]]:
    url = f"{base_url.rstrip('/')}{path}"
    async with Client(url) as client:
        tools = await client.list_tools()
    return url, [tool.name for tool in tools]


async def main_async() -> None:
    args = parse_args()
    results = await asyncio.gather(*(list_tools(args.base_url, path) for path in ENDPOINTS))
    for url, tools in results:
        print(f"{url} -> {len(tools)} tools: {', '.join(tools)}")


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
