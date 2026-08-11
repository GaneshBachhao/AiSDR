"""Legacy Lead response schema aligned with the canonical Lead model."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.domain.lead.enums.lead_source import LeadSource
from app.domain.lead.enums.lead_status import LeadStatus


class LeadResponse(BaseModel):
    """Lead response."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    company_id: str
    contact_id: str
    source: LeadSource
    status: LeadStatus
    score: int
    notes: str | None
    is_qualified: bool
    created_at: datetime
    updated_at: datetime
