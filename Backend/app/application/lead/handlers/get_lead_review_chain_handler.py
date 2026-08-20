"""Get Lead Review Chain application handler (EPIC-16)."""

from __future__ import annotations

from app.application.assessment.assessment_mapper import AssessmentMapper
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.discovery.discovery_mapper import DiscoveryMapper
from app.application.lead.dto.lead_review_chain_response import LeadReviewChainResponseDTO
from app.application.lead.lead_mapper import LeadMapper
from app.application.recommendation.mappers.recommendation_mapper import RecommendationMapper
from app.domain.lead.identifiers.lead_id import LeadId


class GetLeadReviewChainHandler:
    """Assemble the full evidence -> hypothesis -> recommendation chain
    for a Lead, so a reviewer can see everything before approving.

    Each stage is None when the Lead hasn't reached it yet -- e.g. a
    freshly-created Lead has no Discovery, so assessment/recommendation
    are also necessarily None.
    """

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, lead_id: str) -> LeadReviewChainResponseDTO:
        async with self._unit_of_work:
            lead = await self._unit_of_work.lead_repository.get_by_id(LeadId(lead_id))

            if lead is None:
                raise NotFoundException(
                    message="Lead not found.",
                    details={"lead_id": lead_id},
                )

            discovery = await self._unit_of_work.discovery_repository.get_by_lead(lead.id)
            assessment = await self._unit_of_work.assessment_repository.get_by_lead_id(lead.id)
            recommendation = None

            if assessment is not None:
                recommendation = await self._unit_of_work.recommendation_repository.get_by_assessment_id(
                    assessment.id,
                )

            contact = await self._unit_of_work.contact_repository.get_by_id(lead.contact_id)
            suppressed = False
            if contact is not None:
                suppression = await self._unit_of_work.suppression_repository.find_by_email(
                    contact.email.value,
                )
                suppressed = suppression is not None

        return LeadReviewChainResponseDTO(
            lead=LeadMapper.to_response(lead),
            discovery=(DiscoveryMapper.to_response_dto(discovery) if discovery is not None else None),
            assessment=(AssessmentMapper.to_get_response(assessment) if assessment is not None else None),
            recommendation=(
                RecommendationMapper.domain_to_dto(recommendation) if recommendation is not None else None
            ),
            contact_email_suppressed=suppressed,
        )
