"""
Discovery lifecycle status.

Architecture Freeze v5.0
"""

from __future__ import annotations

from enum import StrEnum


class DiscoveryStatus(StrEnum):
    """Supported lifecycle states for a Discovery aggregate."""

    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    ON_HOLD = "ON_HOLD"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
