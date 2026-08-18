from dataclasses import dataclass

from app.domain.lead.identifiers import LeadId
from app.domain.shared.base import DomainEvent


@dataclass(frozen=True)
class LeadCreated(DomainEvent):
    """
    Raised when a new lead is created.
    """

    lead_id: LeadId
