"""
Discovery mapping utilities.
"""

from __future__ import annotations

from app.application.discovery.dto.discovery_dto import DiscoveryDTO


class DiscoveryMapper:
    """
    Maps domain discovery objects into application DTOs.
    """

    def to_dto(
        self,
        session,
    ) -> DiscoveryDTO:
        """
        Map DiscoverySession domain entity to DTO.
        """

        return DiscoveryDTO(
            id=session.id.value,

            lead_id=session.lead_id.value,

            company_id=getattr(
                session,
                "company_id",
                None,
            ),

            status=session.status.value,

            summary=getattr(
                session,
                "summary",
                None,
            ),

            notes=getattr(
                session,
                "notes",
                None,
            ),

            response_count=len(
                getattr(session, "responses", [])
            ),

            pain_points=getattr(
                session,
                "pain_points",
                [],
            ),

            business_goals=getattr(
                session,
                "business_goals",
                [],
            ),

            technologies=getattr(
                session,
                "technologies",
                [],
            ),
        )

    @staticmethod
    def command_to_dto(command):

        return command

    @staticmethod
    def results_to_response(results):

        return results