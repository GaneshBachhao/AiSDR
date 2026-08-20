"""
SuppressionEntry domain aggregate.

A do-not-contact record for one email address. Create-only -- once an
address is suppressed it either stays suppressed or is explicitly lifted
(deleted) by an operator; there's no in-between state to guard, so this
entity has no lifecycle methods the way Lead/Recommendation do.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.contact.value_objects.email import Email
from app.domain.shared.base.aggregate_root import AggregateRoot
from app.domain.suppression.enums.suppression_reason import SuppressionReason
from app.domain.suppression.identifiers.suppression_entry_id import SuppressionEntryId


@dataclass(eq=False)
class SuppressionEntry(AggregateRoot[SuppressionEntryId]):
    """
    Aggregate root representing one do-not-contact email address.
    """

    id: SuppressionEntryId = field(
        default_factory=SuppressionEntryId,
        kw_only=True,
    )

    email: Email

    reason: SuppressionReason = SuppressionReason.MANUAL

    notes: str | None = None

    suppressed_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    def __post_init__(self) -> None:
        if self.notes is not None:
            self.notes = self.notes.strip() or None
