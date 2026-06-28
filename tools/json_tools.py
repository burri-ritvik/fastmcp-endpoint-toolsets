"""Generic JSON tools for the /json/mcp endpoint."""

from __future__ import annotations

import json
from typing import Any

from fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def json_pretty(payload: str, indent: int = 2) -> str:
        """Pretty-print a JSON string."""
        return json.dumps(json.loads(payload), indent=indent, sort_keys=True)

    @mcp.tool()
    def json_shape(payload: str) -> dict[str, Any]:
        """Return top-level JSON type and simple shape metadata."""
        value = json.loads(payload)
        if isinstance(value, dict):
            return {"type": "object", "keys": sorted(value.keys()), "size": len(value)}
        if isinstance(value, list):
            return {"type": "array", "size": len(value)}
        return {"type": type(value).__name__, "size": None}
