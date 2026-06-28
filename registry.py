"""Toolset registry: define endpoint groups here."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from fastmcp import FastMCP

from tools import json_tools, math_tools, text_tools, time_tools

APP_NAME = "FastMCP Endpoint Toolsets"
APP_TAGLINE = "One server. One port. Many focused MCP endpoints."


@dataclass(frozen=True, slots=True)
class Toolset:
    """A named group of tools exposed at /{name}/mcp."""

    name: str
    title: str
    description: str
    tags: tuple[str, ...]
    register: Callable[[FastMCP], None]

    @property
    def endpoint(self) -> str:
        return f"/{self.name}/mcp"


# Add your own endpoint group here.
TOOLSETS: tuple[Toolset, ...] = (
    Toolset(
        name="json",
        title="JSON Toolset",
        description="Format, inspect, and validate JSON payloads.",
        tags=("data", "json", "formatting"),
        register=json_tools.register,
    ),
    Toolset(
        name="text",
        title="Text Toolset",
        description="Count words, lines, characters, and common terms.",
        tags=("content", "text", "analysis"),
        register=text_tools.register,
    ),
    Toolset(
        name="math",
        title="Math Toolset",
        description="Run deterministic numeric summaries and calculations.",
        tags=("numbers", "stats", "utility"),
        register=math_tools.register,
    ),
    Toolset(
        name="time",
        title="Time Toolset",
        description="Return current UTC and timezone-aware timestamps.",
        tags=("time", "date", "timezone"),
        register=time_tools.register,
    ),
)


def create_group_servers() -> dict[str, FastMCP]:
    """Create one FastMCP instance per scoped endpoint."""
    servers = {toolset.name: FastMCP(toolset.title) for toolset in TOOLSETS}
    for toolset in TOOLSETS:
        toolset.register(servers[toolset.name])
    return servers


def create_all_server() -> FastMCP:
    """Create the aggregate /mcp server with every registered tool."""
    server = FastMCP(APP_NAME)
    for toolset in TOOLSETS:
        toolset.register(server)
    return server


def toolset_metadata() -> list[dict[str, object]]:
    return [
        {
            "name": toolset.name,
            "title": toolset.title,
            "description": toolset.description,
            "endpoint": toolset.endpoint,
            "tags": list(toolset.tags),
        }
        for toolset in TOOLSETS
    ]
