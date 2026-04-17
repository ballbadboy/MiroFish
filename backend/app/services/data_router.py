"""
Data Router service for ENDORA.

Routes connector ``Document`` objects to simulations that have subscribed to
matching tag patterns. Decouples data ingestion (connectors) from data
consumption (simulations).

Tag filters normalize to a tuple of OR-groups. All groups must match
(AND across groups); within each group any tag suffices (OR within).
``[["ticker:PTT", "ticker:SCB"], ["sentiment:bearish"]]`` means
(ticker PTT OR SCB) AND (sentiment bearish). A flat list ``["a","b"]`` is
treated as ``[["a"],["b"]]`` (all required).

Subscriptions and the routing log persist under
``Config.UPLOAD_FOLDER/data_router/``; writes are atomic (tmp + os.replace).
"""

from __future__ import annotations

import json
import os
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Any

from ..config import Config
from ..connectors.base import Document
from ..utils.logger import get_logger

logger = get_logger("endora.data_router")


# ── Data models ──────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Subscription:
    """A simulation's interest in documents matching certain tag patterns.

    ``tag_filters`` is normalized to a tuple of OR-groups. All groups must be
    satisfied for a document to match (AND across groups); within a group any
    single tag is sufficient (OR within the group).
    """
    simulation_id: str
    tag_filters: tuple[tuple[str, ...], ...]
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    description: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "simulation_id": self.simulation_id,
            "tag_filters": [list(group) for group in self.tag_filters],
            "created_at": self.created_at,
            "description": self.description,
        }


@dataclass(frozen=True)
class RoutedDocument:
    """A Document that matched at least one Subscription."""
    document_id: str
    document_summary: dict[str, Any]
    matched_subscriptions: tuple[str, ...]
    routed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "document_id": self.document_id,
            "document_summary": self.document_summary,
            "matched_subscriptions": list(self.matched_subscriptions),
            "routed_at": self.routed_at,
        }


# ── Router ───────────────────────────────────────────────────────────────────

class DataRouter:
    """Routes connector Documents to subscribed simulations by tag matching.

    Persistence
    -----------
    Subscriptions and routing logs persist to disk under
    ``Config.UPLOAD_FOLDER/data_router/``. The class is safe to use from
    multiple Flask request handlers — file writes are atomic via tmp+rename.
    """

    DATA_DIR = os.path.join(Config.UPLOAD_FOLDER, "data_router")
    SUBSCRIPTIONS_FILE = "subscriptions.json"
    ROUTING_LOG_FILE = "routing_log.jsonl"
    MAX_LOG_ENTRIES = 1000

    def __init__(self) -> None:
        os.makedirs(self.DATA_DIR, exist_ok=True)

    # ── Subscription management ───────────────────────────────────────────

    def subscribe(
        self,
        simulation_id: str,
        tag_filters: list[list[str]] | list[str],
        description: str = "",
    ) -> Subscription:
        """Register a simulation's interest in documents matching tags.

        ``tag_filters`` accepts either a flat list (all tags required) or a
        nested list of OR-groups. Idempotent — replaces any existing
        subscription for the same simulation_id.
        """
        if not simulation_id or not isinstance(simulation_id, str):
            raise ValueError("simulation_id must be a non-empty string")
        normalized = self._normalize_filters(tag_filters)
        if not normalized:
            raise ValueError("tag_filters must contain at least one tag")

        sub = Subscription(
            simulation_id=simulation_id,
            tag_filters=normalized,
            description=description,
        )

        existing = {s.simulation_id: s for s in self._load_subscriptions()}
        existing[simulation_id] = sub
        self._save_subscriptions(list(existing.values()))

        logger.info(
            f"Subscribed {simulation_id} with {len(normalized)} OR-group(s)"
        )
        return sub

    def unsubscribe(self, simulation_id: str) -> bool:
        """Remove a subscription. Returns True if a subscription was removed."""
        subs = self._load_subscriptions()
        kept = [s for s in subs if s.simulation_id != simulation_id]
        if len(kept) == len(subs):
            return False
        self._save_subscriptions(kept)
        logger.info(f"Unsubscribed {simulation_id}")
        return True

    def list_subscriptions(self) -> list[Subscription]:
        """All current subscriptions, newest first."""
        subs = self._load_subscriptions()
        return sorted(subs, key=lambda s: s.created_at, reverse=True)

    def get_subscription(self, simulation_id: str) -> Subscription | None:
        for sub in self._load_subscriptions():
            if sub.simulation_id == simulation_id:
                return sub
        return None

    # ── Routing (the core hot path) ───────────────────────────────────────

    def route_documents(self, documents: list[Document]) -> list[RoutedDocument]:
        """Match each document against all subscriptions and log routing.

        Returns one RoutedDocument per matching document. Documents matching
        no subscription are silently skipped (but counted in metrics).
        """
        subscriptions = self._load_subscriptions()
        routed: list[RoutedDocument] = []
        skipped = 0

        for doc in documents:
            matches = tuple(
                sub.simulation_id
                for sub in subscriptions
                if _matches_subscription(doc.tags, sub)
            )
            if not matches:
                skipped += 1
                continue
            routed_doc = RoutedDocument(
                document_id=doc.id,
                document_summary=_summarize_document(doc),
                matched_subscriptions=matches,
            )
            routed.append(routed_doc)
            self._append_routing_log(routed_doc)

        logger.info(
            f"Routed {len(routed)} of {len(documents)} documents "
            f"({skipped} skipped, {len(subscriptions)} subscriptions)"
        )
        return routed

    def route_one(self, document: Document) -> RoutedDocument | None:
        """Single-document version of ``route_documents``."""
        results = self.route_documents([document])
        return results[0] if results else None

    # ── Inspection ────────────────────────────────────────────────────────

    def recent_routings(self, limit: int = 100) -> list[RoutedDocument]:
        """Tail of the routing log, newest last as written."""
        if limit <= 0:
            return []
        entries = self._load_routing_log()
        return entries[-limit:]

    def stats(self) -> dict[str, Any]:
        """Aggregate stats: subscription count, routings total + 24h, top tags."""
        subscriptions = self._load_subscriptions()
        routings = self._load_routing_log()
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        routings_24h = sum(1 for r in routings if _parse_iso(r.routed_at) >= cutoff)
        return {
            "total_subscriptions": len(subscriptions),
            "total_routed": len(routings),
            "routings_24h": routings_24h,
            "top_tags": self._compute_top_tags(routings),
        }

    # ── Internal helpers ──────────────────────────────────────────────────

    @staticmethod
    def _normalize_filters(
        tag_filters: list[list[str]] | list[str],
    ) -> tuple[tuple[str, ...], ...]:
        """Convert flat or nested filter lists into a uniform tuple of OR-groups."""
        if not tag_filters:
            return ()
        first = tag_filters[0]
        if isinstance(first, str):
            return tuple((t,) for t in tag_filters if isinstance(t, str) and t)
        if isinstance(first, (list, tuple)):
            groups: list[tuple[str, ...]] = []
            for group in tag_filters:
                if not isinstance(group, (list, tuple)):
                    raise ValueError("Mixed filter shape: expected nested list of lists")
                cleaned = tuple(t for t in group if isinstance(t, str) and t)
                if cleaned:
                    groups.append(cleaned)
            return tuple(groups)
        raise ValueError(f"Invalid tag_filters element type: {type(first).__name__}")

    def _subscriptions_path(self) -> str:
        return os.path.join(self.DATA_DIR, self.SUBSCRIPTIONS_FILE)

    def _routing_log_path(self) -> str:
        return os.path.join(self.DATA_DIR, self.ROUTING_LOG_FILE)

    def _load_subscriptions(self) -> list[Subscription]:
        path = self._subscriptions_path()
        if not os.path.isfile(path):
            return []
        try:
            with open(path, encoding="utf-8") as fh:
                raw = json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            logger.error(f"Failed to load subscriptions: {exc}")
            return []
        result: list[Subscription] = []
        for item in raw:
            try:
                result.append(Subscription(
                    simulation_id=item["simulation_id"],
                    tag_filters=tuple(tuple(g) for g in item.get("tag_filters", [])),
                    created_at=item.get("created_at", ""),
                    description=item.get("description", ""),
                ))
            except (KeyError, TypeError) as exc:
                logger.warning(f"Skipping malformed subscription record: {exc}")
        return result

    def _save_subscriptions(self, subscriptions: list[Subscription]) -> None:
        path = self._subscriptions_path()
        tmp = path + ".tmp"
        payload = [s.to_dict() for s in subscriptions]
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        os.replace(tmp, path)

    def _append_routing_log(self, routed: RoutedDocument) -> None:
        """Append one routing entry with size-bounded rotation (drop oldest)."""
        path = self._routing_log_path()
        existing = self._load_routing_log()
        existing.append(routed)
        if len(existing) > self.MAX_LOG_ENTRIES:
            existing = existing[-self.MAX_LOG_ENTRIES:]
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            for entry in existing:
                fh.write(json.dumps(entry.to_dict(), ensure_ascii=False) + "\n")
        os.replace(tmp, path)

    def _load_routing_log(self) -> list[RoutedDocument]:
        path = self._routing_log_path()
        if not os.path.isfile(path):
            return []
        result: list[RoutedDocument] = []
        try:
            with open(path, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        item = json.loads(line)
                        result.append(RoutedDocument(
                            document_id=item["document_id"],
                            document_summary=item.get("document_summary", {}),
                            matched_subscriptions=tuple(item.get("matched_subscriptions", [])),
                            routed_at=item.get("routed_at", ""),
                        ))
                    except (json.JSONDecodeError, KeyError, TypeError) as exc:
                        logger.warning(f"Skipping malformed routing log line: {exc}")
        except OSError as exc:
            logger.error(f"Failed to read routing log: {exc}")
        return result

    @staticmethod
    def _compute_top_tags(routings: list[RoutedDocument]) -> list[dict[str, Any]]:
        """Count tag frequencies across the routing log; return top 10."""
        counter: Counter[str] = Counter()
        for r in routings:
            for tag in r.document_summary.get("tags", []):
                counter[tag] += 1
        return [{"tag": tag, "count": count} for tag, count in counter.most_common(10)]


# ── Module-level helpers ─────────────────────────────────────────────────────

def _matches_subscription(doc_tags: tuple[str, ...], sub: Subscription) -> bool:
    """True if ``doc_tags`` satisfies every OR-group in ``sub.tag_filters``."""
    doc_tag_set = set(doc_tags)
    for or_group in sub.tag_filters:
        if not any(tag in doc_tag_set for tag in or_group):
            return False
    return True


def _summarize_document(doc: Document) -> dict[str, Any]:
    """Compact, JSON-serializable view of a Document for routing logs."""
    return {
        "title": doc.title,
        "source": doc.source,
        "vertical": doc.vertical,
        "tags": list(doc.tags),
        "timestamp": doc.timestamp,
    }


def _parse_iso(value: str) -> datetime:
    """Parse ISO-8601; fall back to epoch on failure."""
    try:
        dt = datetime.fromisoformat(value)
    except (ValueError, TypeError):
        return datetime.fromtimestamp(0, tz=timezone.utc)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
