"""
Base classes for ENDORA data connectors.

Every connector extends ``BaseConnector`` and must implement two hot methods:

    fetch(params)   -> list of raw payloads from the source
    transform(raw)  -> a normalized ``Document``

Connectors are stateless: they read environment variables for credentials
and accept all per-call parameters via ``params``. This makes them easy to
schedule, parallelize, and unit-test.

Tagging
-------
Each ``Document`` carries a ``tags`` list. The Data Router downstream uses
these tags to decide which simulations should consume the document.
Recommended tag conventions:

    vertical:finance   - which industry vertical
    topic:interest-rate - free-form topic labels
    entity:SCB         - named entities (tickers, companies, places)
    sentiment:positive - optional sentiment hint
"""
from __future__ import annotations

import json
import os
import ssl
import urllib.error
import urllib.request
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any


# ── Shared HTTP helper ───────────────────────────────────────────────────────
# Python on macOS often ships without root certs, so explicitly prefer
# certifi when available; this is a transitive dep of openai/zep-cloud.

def _build_ssl_context() -> ssl.SSLContext:
    try:
        import certifi  # type: ignore
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


_SSL_CONTEXT = _build_ssl_context()


def http_get_json(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    timeout: float = 15.0,
) -> dict[str, Any]:
    """GET ``url``, parse JSON. Use this for all connector HTTP calls."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ENDORA-Connector/1.0", **(headers or {})},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_SSL_CONTEXT) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        # Surface the body for better diagnostics — APIs often put error JSON here.
        try:
            err_body = exc.read().decode("utf-8")
        except Exception:  # noqa: BLE001
            err_body = ""
        raise ConnectorError(
            f"HTTP {exc.code} from {url}: {err_body[:200]}"
        ) from exc
    except urllib.error.URLError as exc:
        raise ConnectorError(f"Network error fetching {url}: {exc.reason}") from exc

    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise ConnectorError(f"Invalid JSON from {url}: {exc}") from exc


VALID_VERTICALS = frozenset({
    "healthcare", "finance", "defense",
    "real-estate", "environment", "politics",
    "general",  # cross-vertical sources like news
})

VALID_SOURCE_TYPES = frozenset({"api", "file", "stream", "webhook"})


# ── Document model ────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Document:
    """Normalized document produced by a connector.

    Immutable by design — connectors return fresh instances rather than
    mutating in place. This keeps the pipeline easy to reason about under
    parallel scheduling.
    """

    id: str
    title: str
    content: str
    source: str                       # connector name, e.g. "news_api"
    vertical: str                     # one of VALID_VERTICALS
    tags: tuple[str, ...]             # frozen list of tag strings
    timestamp: str                    # ISO 8601 UTC
    url: str | None = None
    entities: tuple[str, ...] = ()    # populated later by classifier
    raw_metadata: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def make(
        title: str,
        content: str,
        source: str,
        vertical: str,
        tags: list[str] | tuple[str, ...] = (),
        url: str | None = None,
        entities: list[str] | tuple[str, ...] = (),
        raw_metadata: dict[str, Any] | None = None,
        timestamp: datetime | None = None,
        doc_id: str | None = None,
    ) -> "Document":
        """Construct a Document with sensible defaults."""
        if vertical not in VALID_VERTICALS:
            raise ValueError(
                f"Invalid vertical '{vertical}'. "
                f"Must be one of {sorted(VALID_VERTICALS)}"
            )
        ts = (timestamp or datetime.now(timezone.utc)).isoformat()
        return Document(
            id=doc_id or f"doc_{uuid.uuid4().hex[:12]}",
            title=title,
            content=content,
            source=source,
            vertical=vertical,
            tags=tuple(tags),
            timestamp=ts,
            url=url,
            entities=tuple(entities),
            raw_metadata=dict(raw_metadata or {}),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ── Connector metadata ────────────────────────────────────────────────────────

@dataclass(frozen=True)
class ConnectorInfo:
    """Public metadata describing a connector. Used by the API for listing."""
    name: str
    vertical: str
    source_type: str
    description: str
    requires_auth: bool
    auth_env_var: str | None
    default_params: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ── Base connector class ─────────────────────────────────────────────────────

class BaseConnector(ABC):
    """Abstract base for all ENDORA data connectors.

    Subclasses MUST set the class-level metadata attributes below and
    implement ``fetch`` and ``transform``.
    """

    # Required class metadata — override in subclasses.
    name: str = ""                     # unique identifier, snake_case
    vertical: str = "general"          # which vertical this serves
    source_type: str = "api"           # api | file | stream | webhook
    description: str = ""
    requires_auth: bool = False
    auth_env_var: str | None = None    # env var holding the API key
    default_params: dict[str, Any] = {}  # safe defaults for ``fetch``

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        # Validate metadata at subclass creation time (fail fast).
        if not cls.name:
            raise TypeError(f"{cls.__name__} must set class attribute 'name'")
        if cls.vertical not in VALID_VERTICALS:
            raise TypeError(
                f"{cls.__name__}.vertical='{cls.vertical}' invalid. "
                f"Must be one of {sorted(VALID_VERTICALS)}"
            )
        if cls.source_type not in VALID_SOURCE_TYPES:
            raise TypeError(
                f"{cls.__name__}.source_type='{cls.source_type}' invalid."
            )
        if cls.requires_auth and not cls.auth_env_var:
            raise TypeError(
                f"{cls.__name__} requires_auth=True but auth_env_var is unset"
            )

    # ── Lifecycle helpers ──────────────────────────────────────────────────

    def get_credentials(self) -> str | None:
        """Read the API key from the configured env var."""
        if not self.auth_env_var:
            return None
        return os.environ.get(self.auth_env_var)

    def health_check(self) -> dict[str, Any]:
        """Quick connectivity test. Override for real probes."""
        return {
            "connector": self.name,
            "ok": (not self.requires_auth) or bool(self.get_credentials()),
            "auth_present": bool(self.get_credentials()),
        }

    def info(self) -> ConnectorInfo:
        return ConnectorInfo(
            name=self.name,
            vertical=self.vertical,
            source_type=self.source_type,
            description=self.description,
            requires_auth=self.requires_auth,
            auth_env_var=self.auth_env_var,
            default_params=dict(self.default_params),
        )

    # ── Hot path — must be implemented ─────────────────────────────────────

    @abstractmethod
    def fetch(self, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Fetch raw payloads from the source.

        ``params`` overrides ``default_params`` per call. Return a list of
        dicts in the source's native shape — transform() will normalize.
        Raise ConnectorError on transport failures.
        """

    @abstractmethod
    def transform(self, raw: dict[str, Any]) -> Document:
        """Convert a single raw payload into a normalized Document."""

    # ── Convenience: full pipeline ─────────────────────────────────────────

    def run(self, params: dict[str, Any] | None = None) -> list[Document]:
        """Fetch + transform in one call. Skips items that fail to transform."""
        merged = {**self.default_params, **(params or {})}
        raw_items = self.fetch(merged)
        docs: list[Document] = []
        for raw in raw_items:
            try:
                docs.append(self.transform(raw))
            except Exception as exc:  # noqa: BLE001 - log and continue
                # Connectors should never crash the pipeline on a single bad item.
                # Real logging is plugged in by the registry.
                raw_metadata = {"transform_error": str(exc), "raw_keys": list(raw)}
                docs.append(Document.make(
                    title=f"[transform-error] {self.name}",
                    content=str(raw)[:500],
                    source=self.name,
                    vertical=self.vertical,
                    tags=["error:transform"],
                    raw_metadata=raw_metadata,
                ))
        return docs


class ConnectorError(Exception):
    """Raised when a connector cannot reach its source or auth fails."""
