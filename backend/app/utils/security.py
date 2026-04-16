"""
Security utilities — input validation helpers.
"""

import re
from pathlib import Path
from flask import abort

# Matches safe project/simulation/report IDs: letters, digits, underscore, hyphen, max 80 chars
_ID_RE = re.compile(r'^[A-Za-z0-9_-]{1,80}$')


def safe_id(value: str, label: str = "id") -> str:
    """
    Validate a URL-parameter ID to prevent path traversal.

    Raises a 400 HTTP error if the value is missing or contains
    characters that could escape the uploads directory.

    Args:
        value: The raw ID string from the URL.
        label: Human-readable label used in the error message.

    Returns:
        The validated ID string (unchanged).
    """
    if not value or not _ID_RE.match(value):
        abort(400, description=f"Invalid {label}: must be 1-80 alphanumeric/underscore/hyphen characters")
    return value


def safe_path(base_dir: str, child: str) -> str:
    """
    Resolve *child* relative to *base_dir* and confirm it stays inside.

    Raises a 400 HTTP error if the resolved path escapes the base directory.

    Args:
        base_dir: Trusted base directory (absolute path).
        child: Relative child path to join.

    Returns:
        The resolved absolute path string.
    """
    base = Path(base_dir).resolve()
    target = (base / child).resolve()
    if base != target and base not in target.parents:
        abort(400, description="Invalid path")
    return str(target)
