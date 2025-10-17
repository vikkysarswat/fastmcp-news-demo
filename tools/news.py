"""
News toolset for FastMCP.

Provides:
- list_news(category, limit)
- get_news_by_id(id)
- search_news(query, limit)

Also registers news items as MCP resources under `mcp://news/`.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import List, Optional
from fastmcp import FastMCP
from models.schema import NewsItem

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "news.json"


def _load_news() -> List[NewsItem]:
    items = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    return [NewsItem.model_validate(i) for i in items]


def register_news_tools(mcp: FastMCP) -> None:
    news_db = _load_news()

    # --- MCP Resources (one per article) -------------------------------------
    for item in news_db:
        uri = f"mcp://news/{item.id}"
        mcp.add_resource(
            uri,
            name=item.title,
            description=f"News article ({item.category})",
            mime_type="application/json",
            data=item.model_dump_json().encode("utf-8"),
        )

    # --- Tools ----------------------------------------------------------------

    @mcp.tool
    def list_news(category: Optional[str] = None, limit: int = 20) -> List[NewsItem]:
        """
        List news, optionally filtered by category.

        Args:
            category: Optional category filter (e.g., 'tech').
            limit: Maximum number of items to return.

        Returns:
            A list of NewsItem objects (sorted by published_at desc).
        """
        items = news_db
        if category:
            items = [n for n in items if n.category == category]
        items = sorted(items, key=lambda n: n.published_at, reverse=True)
        return items[:max(1, min(limit, 100))]

    @mcp.tool
    def get_news_by_id(id: str) -> Optional[NewsItem]:
        """
        Retrieve a single news item by its ID.

        Returns:
            The matching NewsItem or None if not found.
        """
        for n in news_db:
            if n.id == id:
                return n
        return None

    @mcp.tool
    def search_news(query: str, limit: int = 20) -> List[NewsItem]:
        """
        Full-text search across title, summary, body, and tags.

        Args:
            query: Search query string.
            limit: Maximum number of results.

        Returns:
            Matching NewsItem objects (naive rank by occurrence count).
        """
        q = query.lower().strip()
        if not q:
            return []
        scored = []
        for n in news_db:
            hay = " ".join(
                [n.title, n.summary, n.body, " ".join(n.tags)]
            ).lower()
            score = hay.count(q)
            if score:
                scored.append((score, n))
        scored.sort(key=lambda t: (t[0], t[1].published_at), reverse=True)
        return [n for _, n in scored[:max(1, min(limit, 100))]]
