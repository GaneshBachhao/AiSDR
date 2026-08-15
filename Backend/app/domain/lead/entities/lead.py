"""
Lead domain aggregate.

A Lead belongs to a Company/Account and references a Contact by ID.
Contact details are intentionally not duplicated on the Lead aggregate.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.lead.enums.lead_source import LeadSource
from app.domain.lead.enums.lead_status import LeadStatus
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.lead.value_objects.lead_score import LeadScore
from app.domain.shared.base.aggregate_root import AggregateRoot


@dataclass(eq=False)
class Lead(AggregateRoot[LeadId]):
    """
    Aggregate root representing a sales lead.

    Business ownership:
    - A Lead belongs to one Company/Account.
    - A Lead references one Contact.
    - Contact name, email, phone, and website are owned by Contact and are
      deliberately not duplicated here.
    """

    id: LeadId = field(
        default_factory=LeadId,
        kw_only=True,
    )

    company_id: CompanyId

    contact_id: ContactId

    source: LeadSource = LeadSource.OTHER

    status: LeadStatus = LeadStatus.NEW

    score: LeadScore = field(
        default_factory=LeadScore,
    )

    notes: str | None = None

    is_qualified: bool = False

    def __post_init__(self) -> None:
        """Normalize Lead-owned text data."""
        if self.notes is not None:
            self.notes = self.notes.strip() or None

    # ---------------------------------------------------------
    # Update operations
    # ---------------------------------------------------------

    def update_contact(
        self,
        contact_id: ContactId,
    ) -> None:
        """Change the Contact associated with this Lead."""
        self.contact_id = contact_id
        self.touch()

    def update_source(
        self,
        source: LeadSource,
    ) -> None:
        """Change the Lead source."""
        self.source = source
        self.touch()

    def update_status(
        self,
        status: LeadStatus,
    ) -> None:
        """Change Lead lifecycle status."""
        self.status = status
        self.is_qualified = status == LeadStatus.QUALIFIED
        self.touch()

    def update_score(
        self,
        score: LeadScore,
    ) -> None:
        """Change Lead qualification score."""
        self.score = score
        self.touch()

    def update_notes(
        self,
        notes: str | None,
    ) -> None:
        """Replace Lead notes."""
        self.notes = notes.strip() if notes else None
        self.touch()

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def qualify(self) -> None:
        """Mark the Lead as qualified."""
        self.status = LeadStatus.QUALIFIED
        self.is_qualified = True
        self.touch()

    def disqualify(self) -> None:
        """Mark the Lead as disqualified."""
        self.status = LeadStatus.DISQUALIFIED
        self.is_qualified = False
        self.touch()

    def convert(self) -> None:
        """Mark the Lead as converted."""
        self.status = LeadStatus.CONVERTED
        self.is_qualified = False
        self.touch()

    def close(self) -> None:
        """Close the Lead."""
        self.status = LeadStatus.CLOSED
        self.touch()
