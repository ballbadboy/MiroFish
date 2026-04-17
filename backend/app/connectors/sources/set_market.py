"""
SET (Stock Exchange of Thailand) Market Connector.

Fetches public OHLC data via Yahoo Finance's free chart API. No API key
needed — the Yahoo endpoint is rate-limited but stable for daily polling.

For each ticker, returns one Document containing the latest day's
summary (price, change, volume) plus the prior close. Tags include
``ticker:SCB`` style entity tags so the downstream router can match
simulations that care about specific stocks.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ..base import BaseConnector, Document, ConnectorError, http_get_json


# Default basket: SET50 large caps. User can override via params['tickers'].
DEFAULT_TICKERS = (
    "PTT.BK", "AOT.BK", "ADVANC.BK", "CPALL.BK", "SCB.BK",
    "KBANK.BK", "BBL.BK", "DELTA.BK", "GULF.BK", "BDMS.BK",
)


class SETMarketConnector(BaseConnector):
    name = "set_market"
    vertical = "finance"
    source_type = "api"
    description = (
        "Stock Exchange of Thailand daily price/volume snapshots via "
        "Yahoo Finance. Free, no API key required."
    )
    requires_auth = False
    auth_env_var = None

    default_params: dict[str, Any] = {
        "tickers": list(DEFAULT_TICKERS),
        "range": "5d",          # 1d | 5d | 1mo | 3mo | 6mo | 1y
        "interval": "1d",
    }

    BASE_URL = "https://query1.finance.yahoo.com/v8/finance/chart"

    # ── fetch ──────────────────────────────────────────────────────────────

    def fetch(self, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        params = params or {}
        tickers = params.get("tickers") or list(DEFAULT_TICKERS)
        rng = params.get("range", "5d")
        interval = params.get("interval", "1d")

        results: list[dict[str, Any]] = []
        for ticker in tickers:
            try:
                results.append(self._fetch_one(ticker, rng, interval))
            except Exception as exc:  # noqa: BLE001
                # Add a marker dict so transform() reports the failure cleanly.
                results.append({"ticker": ticker, "_error": str(exc)})
        return results

    def _fetch_one(self, ticker: str, rng: str, interval: str) -> dict[str, Any]:
        url = f"{self.BASE_URL}/{ticker}?range={rng}&interval={interval}"
        payload = http_get_json(url, timeout=10)

        chart = payload.get("chart", {})
        if chart.get("error"):
            raise ConnectorError(
                f"Yahoo error for {ticker}: {chart['error'].get('description')}"
            )
        result_list = chart.get("result") or []
        if not result_list:
            raise ConnectorError(f"No chart data for {ticker}")

        result = result_list[0]
        meta = result.get("meta", {})
        timestamps = result.get("timestamp", []) or []
        quote = (result.get("indicators", {}).get("quote") or [{}])[0]
        closes = quote.get("close") or []
        opens = quote.get("open") or []
        highs = quote.get("high") or []
        lows = quote.get("low") or []
        volumes = quote.get("volume") or []

        return {
            "ticker": ticker,
            "currency": meta.get("currency"),
            "exchange": meta.get("exchangeName"),
            "regular_market_price": meta.get("regularMarketPrice"),
            "previous_close": meta.get("chartPreviousClose"),
            "timestamps": timestamps,
            "opens": opens,
            "highs": highs,
            "lows": lows,
            "closes": closes,
            "volumes": volumes,
        }

    # ── transform ──────────────────────────────────────────────────────────

    def transform(self, raw: dict[str, Any]) -> Document:
        ticker = raw.get("ticker", "UNKNOWN")
        # Strip the .BK suffix for cleaner display/tags.
        symbol = ticker.replace(".BK", "")

        if raw.get("_error"):
            return Document.make(
                title=f"[fetch-error] {symbol}",
                content=raw["_error"],
                source=self.name,
                vertical=self.vertical,
                tags=[f"ticker:{symbol}", "error:fetch", f"vertical:{self.vertical}"],
                raw_metadata={"ticker": ticker},
            )

        price = raw.get("regular_market_price")
        prev = raw.get("previous_close")
        change = None
        change_pct = None
        if isinstance(price, (int, float)) and isinstance(prev, (int, float)) and prev:
            change = price - prev
            change_pct = (change / prev) * 100.0

        closes = raw.get("closes") or []
        volumes = raw.get("volumes") or []
        # Build a compact human-readable summary as the document content.
        lines = [
            f"Ticker: {symbol} ({ticker})",
            f"Exchange: {raw.get('exchange')} ({raw.get('currency')})",
            f"Latest price: {price:.2f}" if isinstance(price, (int, float)) else "Latest price: n/a",
            f"Previous close: {prev:.2f}" if isinstance(prev, (int, float)) else "Previous close: n/a",
        ]
        if change is not None:
            direction = "+" if change >= 0 else ""
            lines.append(f"Change: {direction}{change:.2f} ({direction}{change_pct:.2f}%)")
        recent_closes = [c for c in closes[-5:] if c is not None]
        recent_volumes = [v for v in volumes[-5:] if v is not None]
        if recent_closes:
            lines.append("Recent closes (oldest→newest): " + ", ".join(f"{c:.2f}" for c in recent_closes))
        if recent_volumes:
            lines.append("Recent volumes: " + ", ".join(f"{v:,}" for v in recent_volumes))

        # Tag with sentiment hint based on price move.
        sentiment_tag = "sentiment:flat"
        if change_pct is not None:
            if change_pct >= 1.0:
                sentiment_tag = "sentiment:bullish"
            elif change_pct <= -1.0:
                sentiment_tag = "sentiment:bearish"

        tags = [
            f"vertical:{self.vertical}",
            f"ticker:{symbol}",
            f"exchange:{(raw.get('exchange') or 'set').lower()}",
            sentiment_tag,
        ]

        return Document.make(
            title=f"{symbol} daily snapshot",
            content="\n".join(lines),
            source=self.name,
            vertical=self.vertical,
            tags=tags,
            entities=[symbol],
            timestamp=datetime.now(timezone.utc),
            raw_metadata={
                "ticker": ticker,
                "price": price,
                "previous_close": prev,
                "change": change,
                "change_pct": change_pct,
                "recent_closes": recent_closes,
                "recent_volumes": recent_volumes,
            },
        )
