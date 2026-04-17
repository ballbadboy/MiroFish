"""
ENDORA Data Connectors
======================

Pluggable data source connectors that fetch from external APIs/feeds and
transform results into normalized Document objects for ingestion into the
simulation pipeline.

Public API:
    BaseConnector       - abstract base for all connectors
    Document            - normalized data payload
    ConnectorInfo       - metadata for listing/discovery
    registry            - global ConnectorRegistry instance
"""

from .base import BaseConnector, Document, ConnectorInfo
from .registry import registry, ConnectorRegistry

__all__ = [
    "BaseConnector",
    "Document",
    "ConnectorInfo",
    "registry",
    "ConnectorRegistry",
]
