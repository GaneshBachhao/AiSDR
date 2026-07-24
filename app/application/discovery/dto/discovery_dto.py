"""
Discovery application DTO models.
"""

from __future__ import annotations

from uuid import UUID

from app.application.common.dto.response_dto import (
    ResponseDTO,
)


class DiscoveryDTO(ResponseDTO):
    """
    Application representation of DiscoverySession.
    """

    id: UUID

    lead_id: UUID

    company_id: str | None = None

    status: str

    summary: str | None = None

    notes: str | None = None

    response_count: int

    pain_points: list[str]

    business_goals: list[str]

    technologies: list[str]