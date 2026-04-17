"""
CoinGecko Crypto Price Connector.

Fetches a market snapshot (price, 24h change, market cap, volume) for a
basket of top crypto assets via CoinGecko's free public endpoint. No API
key required, but the free tier is rate-limited to roughly 10-30 calls
per minute — keep polling cadence modest.

For each configured coin, returns one Document containing a human-readable
summary plus the raw numeric fields in ``raw_metadata``. Tags include
``coin:bitcoin`` / ``symbol:BTC`` style entity tags plus coarse
``sentiment:bullish``/``marketcap:large`` hints so the downstream router
can match simulations that care about specific assets or regimes.
"""
from __future__ import annotations

import urllib.parse
from datetime import datetime, timezone
from typing import Any

from ..base import BaseConnector, Document, ConnectorError, http_get_json


# Default basket: top market-cap names. User can override via params['coins'].
DEFAULT_COINS = (
    "bitcoin", "ethereum", "solana", "binancecoin", "ripple",
)


class CryptoPriceConnector(BaseConnector):
    name = "crypto_price"
    vertical = "finance"
    source_type = "api"
    description = (
        "CoinGecko top crypto market data (price, 24h change, market cap, "
        "volume). Free tier."
    )
    requires_auth = False
    auth_env_var = None

    default_params: dict[str, Any] = {
        "coins": list(DEFAULT_COINS),
        "vs_currency": "usd",
    }

    BASE_URL = "https://api.coingecko.com/api/v3/coins/markets"

    # ── fetch ──────────────────────────────────────────────────────────────

    def fetch(self, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        params = params or {}
        coins = params.get("coins") or list(DEFAULT_COINS)
        vs_currency = params.get("vs_currency", "usd")

        query = {
            "vs_currency": vs_currency,
            "ids": ",".join(coins),
            "order": "market_cap_desc",
            "per_page": 100,
            "page": 1,
            "price_change_percentage": "24h",
        }
        url = f"{self.BASE_URL}?{urllib.parse.urlencode(query)}"
        payload = http_get_json(url, timeout=15)

        if isinstance(payload, dict) and payload.get("error"):
            raise ConnectorError(f"CoinGecko error: {payload.get('error')}")
        if not isinstance(payload, list):
            raise ConnectorError(
                f"Unexpected CoinGecko payload shape: {type(payload).__name__}"
            )

        # Stamp the requested currency on each row so transform() can render it.
        for row in payload:
            if isinstance(row, dict):
                row.setdefault("_vs_currency", vs_currency)
        return payload

    # ── transform ──────────────────────────────────────────────────────────

    def transform(self, raw: dict[str, Any]) -> Document:
        coin_id = raw.get("id", "unknown")
        name = raw.get("name", coin_id)
        symbol = (raw.get("symbol") or coin_id).upper()
        currency = (raw.get("_vs_currency") or "usd").upper()

        price = raw.get("current_price")
        change_pct = raw.get("price_change_percentage_24h")
        change_abs = raw.get("price_change_24h")
        market_cap = raw.get("market_cap")
        market_cap_rank = raw.get("market_cap_rank")
        volume = raw.get("total_volume")
        ath = raw.get("ath")
        ath_change_pct = raw.get("ath_change_percentage")

        lines = [f"{symbol} ({name})"]
        if isinstance(price, (int, float)):
            lines.append(f"Price: ${price:,.2f} {currency}")
        else:
            lines.append("Price: n/a")

        if isinstance(change_pct, (int, float)) and isinstance(change_abs, (int, float)):
            direction = "+" if change_pct >= 0 else ""
            lines.append(
                f"24h change: {direction}{change_pct:.2f}% "
                f"({direction}${change_abs:,.2f})"
            )

        if isinstance(market_cap, (int, float)):
            rank_s = f" (rank #{market_cap_rank})" if market_cap_rank else ""
            lines.append(f"Market cap: {_fmt_big_dollar(market_cap)}{rank_s}")

        if isinstance(volume, (int, float)):
            lines.append(f"24h volume: {_fmt_big_dollar(volume)}")

        if isinstance(ath, (int, float)):
            ath_extra = ""
            if isinstance(ath_change_pct, (int, float)):
                ath_extra = f" ({ath_change_pct:.2f}% from ATH)"
            lines.append(f"All-time high: ${ath:,.2f}{ath_extra}")

        # Sentiment hint based on 24h move.
        sentiment_tag = "sentiment:flat"
        if isinstance(change_pct, (int, float)):
            if change_pct > 2:
                sentiment_tag = "sentiment:bullish"
            elif change_pct < -2:
                sentiment_tag = "sentiment:bearish"

        # Marketcap bucket based on rank.
        if isinstance(market_cap_rank, int) and market_cap_rank <= 10:
            cap_tag = "marketcap:large"
        elif isinstance(market_cap_rank, int) and market_cap_rank <= 100:
            cap_tag = "marketcap:mid"
        else:
            cap_tag = "marketcap:small"

        tags = [
            f"vertical:{self.vertical}",
            "asset:crypto",
            f"coin:{coin_id}",
            f"symbol:{symbol}",
            sentiment_tag,
            cap_tag,
        ]

        return Document.make(
            title=f"{symbol} ({name}) market snapshot",
            content="\n".join(lines),
            source=self.name,
            vertical=self.vertical,
            tags=tags,
            entities=[symbol],
            timestamp=datetime.now(timezone.utc),
            raw_metadata={
                "id": coin_id,
                "symbol": symbol,
                "current_price": price,
                "price_change_24h": change_abs,
                "price_change_percentage_24h": change_pct,
                "market_cap": market_cap,
                "market_cap_rank": market_cap_rank,
                "total_volume": volume,
                "ath": ath,
                "ath_change_percentage": ath_change_pct,
            },
        )


def _fmt_big_dollar(value: float) -> str:
    """Format large dollar amounts like $1.24T / $28.50B / $5.20M."""
    abs_v = abs(value)
    if abs_v >= 1e12:
        return f"${value / 1e12:,.2f}T"
    if abs_v >= 1e9:
        return f"${value / 1e9:,.2f}B"
    if abs_v >= 1e6:
        return f"${value / 1e6:,.2f}M"
    return f"${value:,.2f}"
