from dataclasses import dataclass

from app.domain.common.events.domain_event import DomainEvent


@dataclass(frozen=True)
class CompanyUpdated(DomainEvent):
    """
    Raised when company information is updated.
    """

    company_id: str