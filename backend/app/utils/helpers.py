"""
Common utility functions.
"""

from typing import Any


def filter_none(data: dict[str, Any]) -> dict[str, Any]:
    """Remove keys with None values from a dict — useful for partial updates."""
    return {k: v for k, v in data.items() if v is not None}
