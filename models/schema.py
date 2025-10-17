"""
Pydantic schemas for News and Placards.

These models are used both as return types for FastMCP tools
and for internal validation.
"""

from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Literal, List
from datetime import datetime


class NewsItem(BaseModel):
    id: str = Field(..., description="Stable unique identifier")
    title: str
    category: Literal["world", "business", "sports", "tech", "culture", "science"]
    summary: str
    body: str
    author: str
    published_at: datetime
    image_url: Optional[HttpUrl] = None
    source_url: Optional[HttpUrl] = None
    tags: List[str] = []


class PlacardItem(BaseModel):
    id: str
    title: str
    subtitle: Optional[str] = None
    badge: Optional[str] = None
    kind: Literal["news", "promo", "tip", "warning", "success"] = "news"
    image_url: Optional[HttpUrl] = None
    action_label: Optional[str] = None
    action_url: Optional[HttpUrl] = None
