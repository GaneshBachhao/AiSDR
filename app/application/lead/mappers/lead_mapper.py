from __future__ import annotations

from app.application.lead.dto.lead_dto import LeadDTO
from app.domain.lead.entities.lead import Lead


class LeadMapper:
    """
    Maps between Lead domain entity and application models.
    """

    @staticmethod
    def to_domain(command) -> Lead:
        """
        Convert CreateLeadCommand into Lead aggregate.
        """

        return Lead(
            company_name=command.company_name,
            contact_name=command.contact_name,
            email=command.email,
            phone=command.phone,
            website=command.website,
        )

    @staticmethod
    def to_dto(
        lead: Lead,
    ) -> LeadDTO:
        """
        Convert Lead aggregate into LeadDTO.
        """

        return LeadDTO(
            id=lead.id.value,
            company_name=lead.company_name,
            contact_name=lead.contact_name,
            email=lead.email,
            phone=lead.phone,
            website=lead.website,
            is_qualified=lead.is_qualified,
        )