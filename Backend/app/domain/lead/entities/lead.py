"""
Lead domain aggregate.

A Lead belongs to a Company/Account and references a Contact by ID.
Contact details are intentionally not duplicated on the Lead aggregate.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.lead.enums.lead_review_status import LeadReviewStatus
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

    review_status: LeadReviewStatus = LeadReviewStatus.NOT_SUBMITTED

    review_submitted_at: datetime | None = None

    review_decided_at: datetime | None = None

    review_notes: str | None = None

    # Buying-signal categories detected at creation time by AI research
    # (EPIC-12). None means "not captured" (e.g. a manually-created Lead
    # that never went through company_research) -- distinct from a dict of
    # False, which means every category was checked for and absent.
    evidence_signals: dict[str, bool] | None = None

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
        """Replace Lead notes.

        Matches __post_init__'s normalization: a whitespace-only string
        must clear to None, not survive as "". The previous
        `notes.strip() if notes else None` only checked truthiness before
        stripping, so "   " (truthy) stripped to "" instead of None.
        """
        self.notes = (notes.strip() or None) if notes else None
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

    # ---------------------------------------------------------
    # Human-in-the-loop review gate (EPIC-16)
    #
    # Orthogonal to the CRM lifecycle above -- a Lead's review_status
    # tracks whether a human has cleared it for outreach, independent of
    # whether it's Qualified/Contacted/etc. No code anywhere can move a
    # Lead past APPROVED yet; there is no send mechanism in this codebase
    # to reach or bypass (see EPIC-09).
    # ---------------------------------------------------------

    def submit_for_review(self) -> None:
        """Submit the Lead for human review before any future outreach."""
        if self.review_status in (
            LeadReviewStatus.PENDING_REVIEW,
            LeadReviewStatus.APPROVED,
        ):
            raise ValueError("Lead is already pending review or approved.")
        self.review_status = LeadReviewStatus.PENDING_REVIEW
        self.review_submitted_at = datetime.now(UTC)
        self.touch()

    def approve(self, notes: str | None = None) -> None:
        """Approve a pending-review Lead."""
        if self.review_status != LeadReviewStatus.PENDING_REVIEW:
            raise ValueError("Lead must be pending review before approval.")
        self.review_status = LeadReviewStatus.APPROVED
        self.review_decided_at = datetime.now(UTC)
        if notes:
            self.review_notes = notes
        self.touch()

    def reject(self, notes: str | None = None) -> None:
        """Reject a pending-review Lead. Can be resubmitted afterward."""
        if self.review_status != LeadReviewStatus.PENDING_REVIEW:
            raise ValueError("Lead must be pending review before rejection.")
        self.review_status = LeadReviewStatus.REJECTED
        self.review_decided_at = datetime.now(UTC)
        if notes:
            self.review_notes = notes
        self.touch()
