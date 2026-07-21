"""
Enriched Lead Schema

Represents a LeadCandidate after
AI enrichment.
"""

from app.lead_intelligence.schemas.lead_candidate_schema import (
    LeadCandidate,
)


class EnrichedLead(LeadCandidate):
    """
    Extended LeadCandidate with enriched data.
    """

    description: str | None = None

    products: list[str] = []

    technologies: list[str] = []

    ai_readiness: str | None = None

    estimated_revenue: str | None = None