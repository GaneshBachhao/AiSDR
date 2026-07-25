"""
Assessment application DTO models.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from app.application.common.dto.response_dto import (
    ResponseDTO,
)


class AssessmentDTO(ResponseDTO):
    """
    Application representation of an Assessment.

    This DTO is independent of API contracts.
    """

    id: UUID

    discovery_session_id: UUID

    status: str

    score: float

    maturity_level: str

    summary: str | None = None

    started_at: datetime | None = None

    completed_at: datetime | None = None

    findings_count: int

    opportunities_count: int