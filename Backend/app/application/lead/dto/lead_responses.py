"""
Lead Response DTOs.

Architecture Freeze v5.0
Contains outgoing application response contracts for the Lead aggregate.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.lead.enums.lead_review_status import LeadReviewStatus
from app.domain.lead.enums.lead_source import LeadSource
from app.domain.lead.enums.lead_status import LeadStatus


@dataclass(slots=True)
class LeadResponseDTO:
    """Standard Lead response DTO."""

    id: str
    company_id: str
    contact_id: str
    source: LeadSource
    status: LeadStatus
    score: int
    notes: str | None = None
    is_qualified: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None
    review_status: LeadReviewStatus = LeadReviewStatus.NOT_SUBMITTED
    review_submitted_at: datetime | None = None
    review_decided_at: datetime | None = None
    review_notes: str | None = None
    evidence_signals: dict[str, bool] | None = None
