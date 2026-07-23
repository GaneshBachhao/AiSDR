"""
Discovery Service

Responsible only for discovering companies from the configured provider.
"""

from __future__ import annotations

from app.discovery.providers.provider_factory import (
    DiscoveryProviderFactory,
)

from app.discovery.schemas.discovery_schema import (
    DiscoveryRequest,
    DiscoveryResult,
)


class DiscoveryService:
    """
    Application service responsible for discovering companies.

    This service does not perform qualification,
    enrichment, or lead creation.
    """

    def __init__(self) -> None:
        self._provider = (
            DiscoveryProviderFactory.get_provider()
        )

    def discover(
        self,
        request: DiscoveryRequest,
    ) -> list[DiscoveryResult]:
        """
        Discover companies matching the request.
        """

        return self._provider.discover(
            industry=request.industry,
            location=request.location,
            max_results=request.max_results,
        )