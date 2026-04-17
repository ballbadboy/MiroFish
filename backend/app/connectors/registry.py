"""
Connector Registry — auto-discovery and lookup.

Connectors register themselves by being subclasses of ``BaseConnector``
defined under ``app.connectors.sources``. The registry imports that
package on first access, then enumerates ``BaseConnector.__subclasses__()``.

This means dropping a new file like ``sources/twitter.py`` with a class
``TwitterConnector(BaseConnector)`` is enough — no manual registration.
"""
from __future__ import annotations

import importlib
import pkgutil
from typing import Any

from .base import BaseConnector, ConnectorInfo


class ConnectorRegistry:
    """Singleton-ish registry. Use the module-level ``registry`` instance."""

    def __init__(self) -> None:
        self._connectors: dict[str, BaseConnector] = {}
        self._loaded = False

    # ── Discovery ─────────────────────────────────────────────────────────

    def _load_sources(self) -> None:
        """Import every module under app.connectors.sources to register subclasses."""
        if self._loaded:
            return

        # Import the sources subpackage to trigger subclass registration.
        try:
            sources_pkg = importlib.import_module("app.connectors.sources")
        except ModuleNotFoundError:
            self._loaded = True
            return

        for mod_info in pkgutil.iter_modules(sources_pkg.__path__):
            if mod_info.name.startswith("_"):
                continue
            try:
                importlib.import_module(f"app.connectors.sources.{mod_info.name}")
            except Exception as exc:  # noqa: BLE001 - skip broken modules
                print(f"[connector-registry] failed to load {mod_info.name}: {exc}")

        # Walk the subclass tree and instantiate one of each.
        for cls in self._all_subclasses(BaseConnector):
            if cls.name and cls.name not in self._connectors:
                try:
                    self._connectors[cls.name] = cls()
                except Exception as exc:  # noqa: BLE001
                    print(f"[connector-registry] failed to init {cls.name}: {exc}")

        self._loaded = True

    @staticmethod
    def _all_subclasses(cls: type) -> set[type]:
        seen: set[type] = set()
        stack = [cls]
        while stack:
            parent = stack.pop()
            for child in parent.__subclasses__():
                if child not in seen:
                    seen.add(child)
                    stack.append(child)
        return seen

    # ── Public API ────────────────────────────────────────────────────────

    def get(self, name: str) -> BaseConnector:
        self._load_sources()
        if name not in self._connectors:
            raise KeyError(f"Unknown connector: '{name}'")
        return self._connectors[name]

    def list(self, vertical: str | None = None) -> list[ConnectorInfo]:
        """List all registered connectors, optionally filtered by vertical."""
        self._load_sources()
        items = [c.info() for c in self._connectors.values()]
        if vertical:
            items = [i for i in items if i.vertical == vertical or i.vertical == "general"]
        return sorted(items, key=lambda i: (i.vertical, i.name))

    def health_check_all(self) -> dict[str, Any]:
        """Return health status for every registered connector."""
        self._load_sources()
        return {
            name: conn.health_check()
            for name, conn in self._connectors.items()
        }

    def reload(self) -> None:
        """Force re-discovery (useful in dev)."""
        self._connectors.clear()
        self._loaded = False
        self._load_sources()


# Module-level singleton — import as `from .registry import registry`.
registry = ConnectorRegistry()
