"""Legacy Lead request schema aligned with the canonical Lead model."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from app.domain.lead.enums.lead_source import LeadSource
from app.domain.lead.enums.lead_status import LeadStatus


class CreateLeadRequest(BaseModel):
    """Create Lead request."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    company_id: str
    contact_id: str
    source: LeadSource = LeadSource.OTHER
    notes: str | None = None


class UpdateLeadRequest(BaseModel):
    """Update Lead request."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    contact_id: str | None = None
    source: LeadSource | None = None
    status: LeadStatus | None = None
    score: int | None = None
    notes: str | None = None
