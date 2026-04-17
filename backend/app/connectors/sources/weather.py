"""
Open-Meteo Weather Connector.

Fetches a 7-day daily forecast (temperature, precipitation, wind) for a
basket of locations via Open-Meteo's free, no-API-key forecast endpoint.

For each configured location, returns one Document containing a
human-readable summary plus the raw daily series in ``raw_metadata``.
Tags include ``location:bangkok`` style entity tags and coarse
``weather:rain``/``weather:hot`` style hints so the downstream router
can match simulations that care about specific climates.
"""
from __future__ import annotations

import urllib.parse
from datetime import datetime, timezone
from typing import Any

from ..base import BaseConnector, Document, ConnectorError, http_get_json


# Default basket: Thailand's three most-watched metros. User can override
# via params['locations'] with a list of {name, lat, lon} dicts.
DEFAULT_LOCATIONS: tuple[dict[str, Any], ...] = (
    {"name": "Bangkok", "lat": 13.7563, "lon": 100.5018},
    {"name": "Chiang Mai", "lat": 18.7883, "lon": 98.9853},
    {"name": "Phuket", "lat": 7.8804, "lon": 98.3923},
)

DAILY_FIELDS = (
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "wind_speed_10m_max",
)


class WeatherConnector(BaseConnector):
    name = "weather"
    vertical = "environment"
    source_type = "api"
    description = (
        "Open-Meteo 7-day weather forecast (temperature, precipitation, "
        "wind). Free, no API key required."
    )
    requires_auth = False
    auth_env_var = None

    default_params: dict[str, Any] = {
        "locations": [dict(loc) for loc in DEFAULT_LOCATIONS],
        "days": 7,
    }

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    # ── fetch ──────────────────────────────────────────────────────────────

    def fetch(self, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        params = params or {}
        locations = params.get("locations") or [dict(loc) for loc in DEFAULT_LOCATIONS]
        days = int(params.get("days", 7))

        results: list[dict[str, Any]] = []
        for location in locations:
            try:
                results.append(self._fetch_one(location, days))
            except Exception as exc:  # noqa: BLE001
                # Add a marker dict so transform() reports the failure cleanly.
                results.append({"location": location, "_error": str(exc)})
        return results

    def _fetch_one(self, location: dict[str, Any], days: int) -> dict[str, Any]:
        query = {
            "latitude": location["lat"],
            "longitude": location["lon"],
            "daily": ",".join(DAILY_FIELDS),
            "timezone": "Asia/Bangkok",
            "forecast_days": days,
        }
        url = f"{self.BASE_URL}?{urllib.parse.urlencode(query)}"
        payload = http_get_json(url, timeout=10)

        if payload.get("error"):
            raise ConnectorError(
                f"Open-Meteo error for {location.get('name')}: {payload.get('reason')}"
            )
        if not payload.get("daily"):
            raise ConnectorError(f"No daily data for {location.get('name')}")

        return {"location": location, "data": payload}

    # ── transform ──────────────────────────────────────────────────────────

    def transform(self, raw: dict[str, Any]) -> Document:
        location = raw.get("location") or {}
        name = location.get("name", "Unknown")
        slug = name.lower().replace(" ", "-")

        if raw.get("_error"):
            return Document.make(
                title=f"[fetch-error] {name}",
                content=raw["_error"],
                source=self.name,
                vertical=self.vertical,
                tags=[f"location:{slug}", "error:fetch", f"vertical:{self.vertical}"],
                raw_metadata={"location": location},
            )

        data = raw.get("data") or {}
        daily = data.get("daily") or {}
        dates = daily.get("time") or []
        highs = daily.get("temperature_2m_max") or []
        lows = daily.get("temperature_2m_min") or []
        rains = daily.get("precipitation_sum") or []
        winds = daily.get("wind_speed_10m_max") or []

        lat = location.get("lat", 0.0)
        lon = location.get("lon", 0.0)
        lines = [
            f"{name} 7-day forecast (lat {lat:.2f}, lon {lon:.2f})",
            "",
        ]
        for i, date in enumerate(dates):
            high = highs[i] if i < len(highs) else None
            low = lows[i] if i < len(lows) else None
            rain = rains[i] if i < len(rains) else None
            wind = winds[i] if i < len(winds) else None
            high_s = f"{high:.0f}°C" if isinstance(high, (int, float)) else "n/a"
            low_s = f"{low:.0f}°C" if isinstance(low, (int, float)) else "n/a"
            rain_s = f"{rain:.0f}mm" if isinstance(rain, (int, float)) else "n/a"
            wind_s = f"{wind:.0f}km/h" if isinstance(wind, (int, float)) else "n/a"
            lines.append(
                f"Day {i + 1} ({date}): {high_s} / {low_s}, "
                f"{rain_s} rain, max wind {wind_s}"
            )

        valid_highs = [h for h in highs if isinstance(h, (int, float))]
        valid_rains = [r for r in rains if isinstance(r, (int, float))]
        valid_winds = [w for w in winds if isinstance(w, (int, float))]

        avg_high = sum(valid_highs) / len(valid_highs) if valid_highs else None
        total_rain = sum(valid_rains) if valid_rains else 0.0
        peak_wind = max(valid_winds) if valid_winds else None

        if avg_high is not None and peak_wind is not None:
            lines.append("")
            lines.append(
                f"Summary: avg high {avg_high:.2f}°C, total rainfall "
                f"{total_rain:.2f}mm, peak wind {peak_wind:.2f}km/h"
            )

        # Coarse weather tags for downstream routing.
        rain_tag = "weather:rain" if total_rain > 10 else "weather:dry"
        if avg_high is None:
            heat_tag = "weather:unknown"
        elif avg_high > 33:
            heat_tag = "weather:hot"
        elif avg_high >= 25:
            heat_tag = "weather:mild"
        else:
            heat_tag = "weather:cool"

        tags = [
            f"vertical:{self.vertical}",
            f"location:{slug}",
            rain_tag,
            heat_tag,
        ]

        return Document.make(
            title=f"{name} 7-day forecast",
            content="\n".join(lines),
            source=self.name,
            vertical=self.vertical,
            tags=tags,
            entities=[name],
            timestamp=datetime.now(timezone.utc),
            raw_metadata={
                "location": location,
                "dates": dates,
                "temperature_2m_max": highs,
                "temperature_2m_min": lows,
                "precipitation_sum": rains,
                "wind_speed_10m_max": winds,
                "avg_high": avg_high,
                "total_rain": total_rain,
                "peak_wind": peak_wind,
            },
        )
