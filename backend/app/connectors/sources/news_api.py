"""
NewsAPI Connector — fetches news articles from newsapi.org.

Free tier: 100 requests/day, no commercial use.
Sign up at https://newsapi.org/register and set NEWSAPI_KEY in .env.

Cross-vertical: tag articles with ``vertical:general`` then let the
downstream Data Router classify into specific verticals.
"""
from __future__ import annotations

import urllib.parse
from datetime import datetime, timezone
from typing import Any

from ..base import BaseConnector, Document, ConnectorError, http_get_json


class NewsAPIConnector(BaseConnector):
    name = "news_api"
    vertical = "general"
    source_type = "api"
    description = (
        "NewsAPI.org top-headlines and everything endpoints. "
        "Cross-vertical news ingestion (sentiment, topics, entities)."
    )
    requires_auth = True
    auth_env_var = "NEWSAPI_KEY"

    default_params: dict[str, Any] = {
        "endpoint": "everything",   # 'everything' | 'top-headlines'
        "q": "thailand",            # query string
        "language": "en",
        "page_size": 20,
        "sort_by": "publishedAt",
    }

    BASE_URL = "https://newsapi.org/v2"

    # ── fetch ──────────────────────────────────────────────────────────────

    def fetch(self, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        params = params or {}
        api_key = self.get_credentials()
        if not api_key:
            raise ConnectorError(
                f"NewsAPI key missing — set env var {self.auth_env_var}"
            )

        endpoint = params.get("endpoint", "everything")
        if endpoint not in ("everything", "top-headlines"):
            raise ConnectorError(f"Invalid endpoint: {endpoint}")

        # Build query string. NewsAPI uses different params per endpoint.
        query: dict[str, str] = {
            "apiKey": api_key,
            "pageSize": str(params.get("page_size", 20)),
        }

        if endpoint == "everything":
            query["q"] = params.get("q", "thailand")
            query["language"] = params.get("language", "en")
            query["sortBy"] = params.get("sort_by", "publishedAt")
            if params.get("from_date"):
                query["from"] = params["from_date"]
            if params.get("to_date"):
                query["to"] = params["to_date"]
        else:  # top-headlines
            if params.get("country"):
                query["country"] = params["country"]
            if params.get("category"):
                query["category"] = params["category"]
            if params.get("q"):
                query["q"] = params["q"]

        url = f"{self.BASE_URL}/{endpoint}?{urllib.parse.urlencode(query)}"
        payload = http_get_json(url, timeout=15)

        if payload.get("status") != "ok":
            raise ConnectorError(
                f"NewsAPI error: {payload.get('code')} — {payload.get('message')}"
            )

        return list(payload.get("articles", []))

    # ── transform ──────────────────────────────────────────────────────────

    def transform(self, raw: dict[str, Any]) -> Document:
        title = raw.get("title") or "Untitled"
        # Combine description + content for richer reality seed.
        content_parts = [
            raw.get("description") or "",
            raw.get("content") or "",
        ]
        content = "\n\n".join(p for p in content_parts if p).strip() or title

        # Tags: vertical + source publisher + author if known.
        publisher = (raw.get("source") or {}).get("name") or "unknown"
        tags = [
            f"vertical:{self.vertical}",
            f"publisher:{publisher.lower().replace(' ', '-')}",
        ]
        author = raw.get("author")
        if author:
            tags.append(f"author:{author.lower()[:40]}")

        # Parse timestamp if provided.
        published_at = raw.get("publishedAt")
        ts: datetime | None = None
        if published_at:
            try:
                # NewsAPI gives "2024-09-01T12:34:56Z"
                ts = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
            except ValueError:
                ts = None

        return Document.make(
            title=title,
            content=content,
            source=self.name,
            vertical=self.vertical,
            tags=tags,
            url=raw.get("url"),
            timestamp=ts or datetime.now(timezone.utc),
            raw_metadata={
                "publisher": publisher,
                "author": author,
                "image_url": raw.get("urlToImage"),
            },
        )

    # ── health ────────────────────────────────────────────────────────────

    def health_check(self) -> dict[str, Any]:
        base = super().health_check()
        # Cheap probe: just check the key is set. A real probe would call
        # /sources, but that costs a request from our 100/day quota.
        return base
