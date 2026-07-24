"""
Discovery domain/application mapper.
"""

from __future__ import annotations

from app.application.discovery.dto.discovery_dto import (
    DiscoveryDTO,
)

from app.domain.discovery.entities.discovery_session import (
    DiscoverySession,
)


class DiscoveryMapper:
    """
    Maps DiscoverySession aggregate
    to application DTO.
    """

    @staticmethod
    def to_dto(
        session: DiscoverySession,
    ) -> DiscoveryDTO:
        """
        Convert DiscoverySession into DiscoveryDTO.
        """

        return DiscoveryDTO(
            id=session.id.value,
            lead_id=session.lead_id.value,
            company_id=session.company_id,
            status=session.status.value,
            summary=session.summary,
            notes=session.notes,
            response_count=len(session.responses),
            pain_points=[
                str(item)
                for item in session.pain_points
            ],
            business_goals=[
                str(item)
                for item in session.business_goals
            ],
            technologies=[
                str(item)
                for item in session.technologies
            ],
        )