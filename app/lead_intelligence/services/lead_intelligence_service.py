"""
Lead Intelligence Service

Coordinates lead discovery using
registered providers.
"""

from app.lead_intelligence.providers.base_provider import (
    BaseLeadProvider,
)

from app.lead_intelligence.providers.manual_provider import (
    ManualLeadProvider,
)

from app.lead_intelligence.schemas.lead_candidate_schema import (
    LeadCandidate,
)

from app.lead_intelligence.schemas.lead_search_request_schema import (
    LeadSearchRequest,
)


class LeadIntelligenceService:
    """
    Orchestrates lead providers.
    """

    def __init__(self):

        self.providers: dict[str, BaseLeadProvider] = {
            "manual": ManualLeadProvider(),
        }

    def register_provider(
        self,
        name: str,
        provider: BaseLeadProvider,
    ) -> None:
        """
        Register a new lead provider.
        """

        self.providers[name] = provider

    def search(
        self,
        provider: str,
        request: LeadSearchRequest,
    ) -> list[LeadCandidate]:
        """
        Search for lead candidates using
        the selected provider.
        """

        if provider not in self.providers:

            raise ValueError(
                f"Unknown provider: {provider}"
            )

        return self.providers[
            provider
        ].search(request)