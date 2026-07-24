"""
Discovery response application DTO.
"""

from __future__ import annotations

from uuid import UUID

from app.application.common.dto.response_dto import (
    ResponseDTO,
)


class DiscoveryResponseDTO(ResponseDTO):
    """
    Application representation of discovery response.
    """

    id: UUID

    question_id: str

    question: str

    answer: str

    response_type: str

    confidence: float

    remarks: str | None = None