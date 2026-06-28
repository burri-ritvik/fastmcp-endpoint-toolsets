"""Generic math tools for the /math/mcp endpoint."""

from __future__ import annotations

from statistics import mean, median

from fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def math_summary(numbers: list[float]) -> dict[str, float | int]:
        """Summarize a list of numbers."""
        if not numbers:
            raise ValueError("numbers must not be empty")
        return {
            "count": len(numbers),
            "min": min(numbers),
            "max": max(numbers),
            "mean": mean(numbers),
            "median": median(numbers),
            "sum": sum(numbers),
        }

    @mcp.tool()
    def math_percent_change(previous: float, current: float) -> float:
        """Return percentage change from previous to current."""
        if previous == 0:
            raise ValueError("previous must not be zero")
        return ((current - previous) / previous) * 100
