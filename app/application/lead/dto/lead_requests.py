"""Lead request DTOs."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.lead.enums.lead_source import LeadSource
from app.domain.lead.enums.lead_status import LeadStatus


@dataclass(slots=True)
class CreateLeadRequestDTO:
    """Request to create a Lead."""

    company_id: str
    contact_id: str
    source: LeadSource = LeadSource.OTHER
    score: int = 0
    notes: str | None = None


@dataclass(slots=True)
class UpdateLeadRequestDTO:
    """Request to update a Lead."""

    contact_id: str | None = None
    source: LeadSource | None = None
    status: LeadStatus | None = None
    score: int | None = None
    notes: str | None = None
