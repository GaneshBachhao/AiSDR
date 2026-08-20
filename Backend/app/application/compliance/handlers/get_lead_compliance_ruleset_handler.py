"""Get Lead Compliance Ruleset application handler (EPIC-11)."""

from __future__ import annotations

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.compliance.compliance_mapper import ComplianceMapper
from app.application.compliance.dto.compliance_responses import (
    LeadComplianceRulesetResponseDTO,
)
from app.domain.compliance.services.jurisdiction_resolver import JurisdictionResolver
from app.domain.lead.identifiers.lead_id import LeadId


class GetLeadComplianceRulesetHandler:
    """Resolve the compliance ruleset that applies to a Lead, via its
    Company's geography -- the only source that's actually authoritative
    at send time (Company.country), not the ephemeral, request-time-only
    CompanyResearchRequest.geography.
    """

    def __init__(self, unit_of_work: UnitOfWork, jurisdiction_resolver: JurisdictionResolver) -> None:
        self._unit_of_work = unit_of_work
        self._jurisdiction_resolver = jurisdiction_resolver

    async def handle(self, lead_id: str) -> LeadComplianceRulesetResponseDTO:
        async with self._unit_of_work:
            lead = await self._unit_of_work.lead_repository.get_by_id(LeadId(lead_id))

            if lead is None:
                raise NotFoundException(
                    message="Lead not found.",
                    details={"lead_id": lead_id},
                )

            company = await self._unit_of_work.company_repository.get_by_id(lead.company_id)

        country = company.country if company is not None else None
        ruleset = self._jurisdiction_resolver.resolve(country)

        return LeadComplianceRulesetResponseDTO(
            lead_id=lead_id,
            company_country=country,
            ruleset=ComplianceMapper.to_response(ruleset),
        )
