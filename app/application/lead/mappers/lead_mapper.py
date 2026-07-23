from __future__ import annotations

from app.application.lead.dto.lead_dto import (
    LeadDTO,
)


class LeadMapper:
    """
    Maps Lead domain entities to application DTOs.
    """

    @staticmethod
    def to_dto(
        lead,
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