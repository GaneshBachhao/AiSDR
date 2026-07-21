from dataclasses import dataclass

from app.domain.shared.base import DomainEvent
from app.domain.lead.identifiers import LeadId


@dataclass(frozen=True)
class LeadCreated(DomainEvent):
    """
    Raised when a new lead is created.
    """

    lead_id: LeadId