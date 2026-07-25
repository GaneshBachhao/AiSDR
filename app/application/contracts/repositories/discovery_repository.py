"""
Discovery repository contract.
"""

from __future__ import annotations

from app.application.common.interfaces.repository import (
    Repository,
)
from app.domain.discovery.entities.discovery import Discovery
from app.domain.discovery.identifiers.discovery_id import DiscoveryId


class DiscoveryRepository(
    Repository[Discovery, DiscoveryId],
):
    """
    Discovery persistence contract.
    """

    pass