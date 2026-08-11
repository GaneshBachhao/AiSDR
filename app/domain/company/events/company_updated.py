from dataclasses import dataclass

from app.domain.shared.base.domain_event import DomainEvent


@dataclass(frozen=True)
class CompanyUpdated(DomainEvent):
    """
    Raised when company information is updated.
    """

    company_id: str