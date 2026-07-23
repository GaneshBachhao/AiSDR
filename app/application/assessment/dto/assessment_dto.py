"""
Assessment DTO.
"""

from __future__ import annotations

from uuid import UUID

from app.application.common.dto.response_dto import (
    ResponseDTO,
)


class AssessmentDTO(ResponseDTO):
    """
    Application representation of an Assessment.
    """

    id: UUID

    discovery_session_id: UUID

    status: str

    overall_score: float

    maturity_level: str

    summary: str | None = None