"""
OutcomeEvent domain aggregate.

An append-only record of what happened for a Lead after outreach --
meeting booked, won, lost, or no response. Unlike SuppressionEntry, this is
not a single flag: the same Lead can accumulate several events over time
(e.g. "No Response" today, "Meeting Booked" next month), so there is no
uniqueness check and no lifecycle methods -- each event is an immutable
fact once recorded.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.outcome.enums.outcome_type import OutcomeType
from app.domain.outcome.identifiers.outcome_event_id import OutcomeEventId
from app.domain.shared.base.aggregate_root import AggregateRoot


@dataclass(eq=False)
class OutcomeEvent(AggregateRoot[OutcomeEventId]):
    """
    Aggregate root representing one recorded outcome for a Lead.
    """

    id: OutcomeEventId = field(
        default_factory=OutcomeEventId,
        kw_only=True,
    )

    lead_id: LeadId

    outcome_type: OutcomeType

    notes: str | None = None

    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    def __post_init__(self) -> None:
        if self.notes is not None:
            self.notes = self.notes.strip() or None
