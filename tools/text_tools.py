"""Generic text tools for the /text/mcp endpoint."""

from __future__ import annotations

from collections import Counter
import re

from fastmcp import FastMCP

WORD_PATTERN = re.compile(r"[A-Za-z0-9_']+")


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def text_stats(text: str) -> dict[str, int]:
        """Count characters, lines, and words."""
        words = WORD_PATTERN.findall(text)
        return {"characters": len(text), "lines": len(text.splitlines()) or 1, "words": len(words)}

    @mcp.tool()
    def text_keywords(text: str, limit: int = 5) -> list[dict[str, int]]:
        """Return the most common words in text."""
        words = [word.lower() for word in WORD_PATTERN.findall(text)]
        return [{"word": word, "count": count} for word, count in Counter(words).most_common(limit)]
