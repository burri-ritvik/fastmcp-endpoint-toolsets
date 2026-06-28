"""
FastMCP Endpoint Toolsets

One server. One port. Native scoped MCP endpoints.

Run:
    python server.py

MCP endpoints:
    /mcp              -> all tools
    /<toolset>/mcp    -> only that toolset's tools

Toolsets are defined in registry.py; each one is exposed at /<name>/mcp.
"""

from __future__ import annotations

import argparse
import contextlib
import inspect
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.routing import Mount, Route

from registry import APP_NAME, APP_TAGLINE, TOOLSETS, create_all_server, create_group_servers, toolset_metadata

# 1. One FastMCP instance per endpoint group.
mcp_groups = create_group_servers()

# 2. One aggregate FastMCP instance for backward-compatible /mcp usage.
all_mcp = create_all_server()

# 3. Convert every FastMCP instance into a native Streamable HTTP MCP app.
http_apps = {
    name: mcp.http_app(path="/mcp", stateless_http=True, transport="streamable-http")
    for name, mcp in mcp_groups.items()
}
all_app = all_mcp.http_app(path="/mcp", stateless_http=True, transport="streamable-http")

# 4. Share lifespan across mounted MCP apps.
ALL_SUB_APPS = list(http_apps.values()) + [all_app]


@asynccontextmanager
async def combined_lifespan(app: Starlette):
    async with contextlib.AsyncExitStack() as stack:
        for sub_app in ALL_SUB_APPS:
            await stack.enter_async_context(sub_app.lifespan(app))
        yield


# 5. Browser-friendly endpoints.
async def homepage(request: Request) -> HTMLResponse:
    html = Path("static/index.html").read_text(encoding="utf-8")
    return HTMLResponse(html)


async def health(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok", "service": "fastmcp-endpoint-toolsets"})


async def favicon(request: Request) -> Response:
    # No favicon by design -- answer the browser's automatic request quietly (no 404 noise).
    return Response(status_code=204)


async def get_tool_names(mcp: Any) -> list[str]:
    list_method = getattr(mcp, "list_tools", None) or getattr(mcp, "get_tools")
    tools = list_method()
    if inspect.isawaitable(tools):
        tools = await tools
    if isinstance(tools, dict):
        return list(tools)
    return [tool.name for tool in tools]


async def list_toolsets_api(request: Request) -> JSONResponse:
    groups: list[dict[str, Any]] = []
    for toolset in TOOLSETS:
        meta = next(item for item in toolset_metadata() if item["name"] == toolset.name)
        groups.append({**meta, "tools": await get_tool_names(mcp_groups[toolset.name])})

    return JSONResponse(
        {
            "name": APP_NAME,
            "tagline": APP_TAGLINE,
            "all": {"endpoint": "/mcp", "tools": await get_tool_names(all_mcp)},
            "toolsets": groups,
        }
    )


# 6. Assemble one Starlette app with many MCP endpoints.
routes = [
    Route("/", homepage, methods=["GET"]),
    Route("/health", health, methods=["GET"]),
    Route("/toolsets", list_toolsets_api, methods=["GET"]),
    Route("/favicon.ico", favicon, methods=["GET"]),
]

for toolset in TOOLSETS:
    routes.append(Mount(f"/{toolset.name}", app=http_apps[toolset.name]))

routes.append(Mount("/", app=all_app))

app = Starlette(routes=routes, lifespan=combined_lifespan)


# 7. Run locally.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run FastMCP Endpoint Toolsets.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8001, type=int)
    return parser.parse_args()


def print_banner(host: str, port: int) -> None:
    shown = "127.0.0.1" if host in ("0.0.0.0", "") else host
    base = f"http://{shown}:{port}"
    lines = [
        "",
        f"  {APP_NAME}",
        f"  {APP_TAGLINE}",
        "",
        f"  Dashboard   {base}/",
        f"  Health      {base}/health",
        f"  Discovery   {base}/toolsets",
        f"  All tools   {base}/mcp",
        "",
        f"  Scoped MCP endpoints: {base}/<toolset>/mcp",
    ]
    lines.append("")
    print("\n".join(lines), flush=True)


def main() -> None:
    args = parse_args()
    print_banner(args.host, args.port)
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()

