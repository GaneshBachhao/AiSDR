# app/application/assessment/dto/finding_dto.py

"""
Finding application DTO models.
"""

from __future__ import annotations

from uuid import UUID

from app.application.common.dto.response_dto import (
    ResponseDTO,
)


class FindingDTO(ResponseDTO):
    """
    Application representation of a Finding.
    """

    finding_id: UUID

    title: str

    description: str

    finding_type: str

    severity: int

    recommendation_hint: str | None = None

    evidence_count: int