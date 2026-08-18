from dataclasses import dataclass
from uuid import UUID

from app.domain.lead.identifiers import LeadId
from app.domain.shared.base import DomainEvent


@dataclass(frozen=True)
class LeadConverted(DomainEvent):
    """
    Raised when a lead is converted into a company.
    """

    lead_id: LeadId

    company_id: UUID
