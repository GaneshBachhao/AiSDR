from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.lead.enums.lead_source import LeadSource
from app.domain.lead.enums.lead_status import LeadStatus
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.lead.value_objects.lead_score import LeadScore
from app.domain.shared.base.aggregate_root import AggregateRoot


@dataclass(eq=False)
class Lead(AggregateRoot[LeadId]):
    """
    Aggregate root representing a prospective AI consulting client.
    """

    id: LeadId = field(
        default_factory=LeadId,
        kw_only=True,
    )

    company_name: str

    contact_name: str

    email: str

    phone: str | None = None

    website: str | None = None

    source: LeadSource = LeadSource.OTHER

    status: LeadStatus = LeadStatus.NEW

    score: LeadScore = field(
        default_factory=LeadScore,
    )

    notes: str | None = None

    is_qualified: bool = False

    def qualify(self) -> None:
        """
        Mark lead as qualified.
        """
        self.is_qualified = True
        self.status = LeadStatus.QUALIFIED
        self.touch()

    def disqualify(self) -> None:
        """
        Mark lead as disqualified.
        """
        self.is_qualified = False
        self.status = LeadStatus.DISQUALIFIED
        self.touch()

    def update_score(
        self,
        score: LeadScore,
    ) -> None:
        """
        Update lead score.
        """
        self.score = score
        self.touch()

    def update_contact(
        self,
        *,
        contact_name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
    ) -> None:
        """
        Update contact information.
        """

        if contact_name is not None:
            self.contact_name = contact_name

        if email is not None:
            self.email = email

        if phone is not None:
            self.phone = phone

        self.touch()

    def add_note(
        self,
        note: str,
    ) -> None:
        """
        Append note.
        """

        if self.notes:
            self.notes += f"\n{note}"
        else:
            self.notes = note

        self.touch()