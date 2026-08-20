"""
Lead review chain response DTO (EPIC-16).

Composes a Lead with whatever downstream pipeline stages it has actually
reached -- Discovery, Assessment, Recommendation -- so a reviewer can see
the evidence -> hypothesis -> recommendation chain in one call before
approving. Each stage is None when the Lead hasn't reached it yet; there
is deliberately no "message" field, since no outreach/messaging mechanism
exists anywhere in this codebase yet (EPIC-09).

``contact_email_suppressed`` (EPIC-11) is a real, non-speculative use of
the suppression list through a screen that already exists: whether the
Lead's contact is on the do-not-contact list is exactly what a reviewer
needs to know before approving, even though no actual send path exists
yet to enforce it automatically.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.assessment.dto.assessment_response import GetAssessmentResponseDTO
from app.application.discovery.dto.discovery_responses import DiscoveryResponseDTO
from app.application.lead.dto.lead_responses import LeadResponseDTO
from app.application.recommendation.dto.recommendation_dto import RecommendationDTO


@dataclass(slots=True)
class LeadReviewChainResponseDTO:
    """The full evidence -> hypothesis -> recommendation chain for a Lead."""

    lead: LeadResponseDTO
    discovery: DiscoveryResponseDTO | None
    assessment: GetAssessmentResponseDTO | None
    recommendation: RecommendationDTO | None
    contact_email_suppressed: bool = False
