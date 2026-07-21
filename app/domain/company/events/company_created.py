from dataclasses import dataclass

from app.domain.common.events.domain_event import DomainEvent


@dataclass(frozen=True)
class CompanyCreated(DomainEvent):
    """
    Raised when a new company is created.
    """

    company_id: str

    company_name: str