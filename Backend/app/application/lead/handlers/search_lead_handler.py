"""
Search Lead application handler.

Architecture Freeze v5.0
"""

from __future__ import annotations

from app.application.common.exceptions.validation_exception import ValidationException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.lead.dto.lead_responses import LeadResponseDTO
from app.application.lead.lead_mapper import LeadMapper
from app.application.lead.lead_queries import SearchLeadQuery
from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.identifiers.contact_id import ContactId


class SearchLeadHandler:
    """Search Leads with optional Company/Contact filters."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, query: SearchLeadQuery) -> list[LeadResponseDTO]:
        try:
            company_id = (
                CompanyId(query.company_id)
                if query.company_id
                else None
            )
            contact_id = (
                ContactId(query.contact_id)
                if query.contact_id
                else None
            )
        except (TypeError, ValueError) as exc:
            raise ValidationException(
                message="Lead filter validation failed.",
                details={"error": str(exc)},
            ) from exc

        async with self._unit_of_work:
            leads = await self._unit_of_work.lead_repository.search(
                query.search_term,
                company_id=company_id,
                contact_id=contact_id,
                skip=query.skip,
                limit=query.limit,
            )

        return LeadMapper.to_response_list(leads)
