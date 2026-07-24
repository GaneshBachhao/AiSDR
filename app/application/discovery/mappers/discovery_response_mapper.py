"""
Discovery response mapper.
"""

from __future__ import annotations

from app.application.discovery.dto.discovery_response_dto import (
    DiscoveryResponseDTO,
)

from app.domain.discovery.entities.discovery_response import (
    DiscoveryResponse,
)


class DiscoveryResponseMapper:
    """
    Maps DiscoveryResponse domain entity
    to application DTO.
    """

    @staticmethod
    def to_dto(
        response: DiscoveryResponse,
    ) -> DiscoveryResponseDTO:
        """
        Convert domain entity into DTO.
        """

        return DiscoveryResponseDTO(
            id=response.response_id,
            question_id=response.question_id,
            question=response.question,
            answer=response.answer,
            response_type=response.response_type.value,
            confidence=response.confidence,
            remarks=response.remarks,
        )