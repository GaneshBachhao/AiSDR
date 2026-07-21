"""
Manual Lead Provider

Creates a LeadCandidate from manually
entered company information.
"""

from app.lead_intelligence.providers.base_provider import (
    BaseLeadProvider,
)

from app.lead_intelligence.schemas.lead_candidate_schema import (
    LeadCandidate,
)

from app.lead_intelligence.schemas.lead_search_request_schema import (
    LeadSearchRequest,
)


class ManualLeadProvider(BaseLeadProvider):
    """
    Manual lead provider.

    Used when the user manually enters
    company information.
    """

    def search(
        self,
        request: LeadSearchRequest,
    ) -> list[LeadCandidate]:

        if not request.company_name:
            return []

        candidate = LeadCandidate(
            company_name=request.company_name,
            website=request.website,
            industry=request.industry,
            country=request.country,
            state=request.state,
            city=request.city,
            source="manual",
            confidence=1.0,
            metadata={},
        )

        return [candidate]