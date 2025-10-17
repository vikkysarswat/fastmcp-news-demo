"""
Placards toolset for FastMCP.

Provides:
- list_placards(kind)

Also registers placards as MCP resources under `mcp://placards/`.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import List, Optional
from fastmcp import FastMCP
from models.schema import PlacardItem

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "placards.json"


def _load_placards() -> List[PlacardItem]:
    items = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    return [PlacardItem.model_validate(i) for i in items]


def register_placard_tools(mcp: FastMCP) -> None:
    db = _load_placards()

    # MCP Resources for each placard (useful for Apps that bind resources to UI)
    for p in db:
        uri = f"mcp://placards/{p.id}"
        mcp.add_resource(
            uri,
            name=p.title,
            description=f"Placard item ({p.kind})",
            mime_type="application/json",
            data=p.model_dump_json().encode("utf-8"),
        )

    @mcp.tool
    def list_placards(kind: Optional[str] = None) -> List[PlacardItem]:
        """
        Return placards, optionally filtered by 'kind' (news, promo, tip, warning, success).
        """
        items = db
        if kind:
            items = [p for p in items if p.kind == kind]
        return items
