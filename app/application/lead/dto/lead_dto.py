# app/application/lead/dto/lead_dto.py

"""
Lead application DTO models.
"""

from __future__ import annotations

from uuid import UUID

from app.application.common.dto.response_dto import (
    ResponseDTO,
)


class LeadDTO(ResponseDTO):
    """
    Application representation of a Lead.

    This DTO is not tied to API contracts.
    API schemas will be created separately.
    """

    id: UUID

    company_name: str

    contact_name: str

    email: str

    phone: str | None = None

    website: str | None = None

    is_qualified: bool