from dataclasses import dataclass

from app.domain.lead.identifiers import LeadId
from app.domain.shared.base import DomainEvent


@dataclass(frozen=True)
class LeadQualified(DomainEvent):
    """
    Raised when a lead is qualified.
    """

    lead_id: LeadId
