"""
Company Intelligence Service

Coordinates the enrichment workflow.
"""

from app.company_intelligence.providers.provider_factory import (
    CompanyIntelligenceProviderFactory,
)

from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)

from app.lead_intelligence.schemas.lead_candidate_schema import (
    LeadCandidate,
)


class CompanyIntelligenceService:
    """
    Builds a CompanyProfile from a LeadCandidate.
    """

    def __init__(self):

        self.provider = (
            CompanyIntelligenceProviderFactory.get_provider()
        )

    def enrich(
        self,
        candidate: LeadCandidate,
    ) -> CompanyProfile:

        return self.provider.enrich(candidate)