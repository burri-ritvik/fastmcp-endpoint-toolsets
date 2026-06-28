"""Generic time tools for the /time/mcp endpoint."""

from __future__ import annotations

from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def time_utc_now() -> str:
        """Return the current UTC timestamp."""
        return datetime.now(UTC).isoformat()

    @mcp.tool()
    def time_in_timezone(timezone: str = "UTC") -> str:
        """Return the current timestamp for an IANA timezone."""
        return datetime.now(ZoneInfo(timezone)).isoformat()
