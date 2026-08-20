"""
Sequence domain aggregate.

An ordered, planned cadence of touches against one Lead. Wait-time rules
and reply/no-reply/bounce branching (EPIC-09.1) -- deliberately does not
generate touch content (EPIC-09.2, needs live AI) or actually send
anything (EPIC-09.3, needs real channel credentials). Nothing in this
codebase automatically drives advance()/record_reply()/record_bounce()
yet -- same "forward-looking infrastructure, no automated caller yet"
shape as Lead's own review gate before EPIC-09 existed to consume it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.sequence.enums.sequence_status import SequenceStatus
from app.domain.sequence.identifiers.sequence_id import SequenceId
from app.domain.sequence.value_objects.touch import Touch
from app.domain.shared.base.aggregate_root import AggregateRoot


@dataclass(eq=False)
class Sequence(AggregateRoot[SequenceId]):
    """
    Aggregate root representing a planned multichannel touch cadence for a Lead.
    """

    id: SequenceId = field(
        default_factory=SequenceId,
        kw_only=True,
    )

    lead_id: LeadId

    touches: list[Touch]

    status: SequenceStatus = SequenceStatus.DRAFT

    current_touch_index: int = 0

    started_at: datetime | None = None

    ended_at: datetime | None = None

    stop_reason: str | None = None

    def __post_init__(self) -> None:
        if not self.touches:
            raise ValueError("Sequence must have at least one touch.")

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def start(self) -> None:
        """Begin the sequence's touch cadence."""
        if self.status != SequenceStatus.DRAFT:
            raise ValueError("Sequence must be in Draft status to start.")
        self.status = SequenceStatus.ACTIVE
        self.started_at = datetime.now(UTC)
        self.touch()

    def advance(self) -> None:
        """Mark the current touch as sent and move to the next one.

        Reaching the end of ``touches`` with no reply/bounce is the "no
        response" branch -- the sequence completes naturally rather than
        being stopped early.
        """
        if self.status != SequenceStatus.ACTIVE:
            raise ValueError("Sequence must be active to advance.")
        self.current_touch_index += 1
        if self.current_touch_index >= len(self.touches):
            self.status = SequenceStatus.COMPLETED
            self.ended_at = datetime.now(UTC)
        self.touch()

    def record_reply(self) -> None:
        """Stop the sequence early: the Lead replied."""
        self._stop("replied")

    def record_bounce(self) -> None:
        """Stop the sequence early: a touch bounced."""
        self._stop("bounced")

    def _stop(self, reason: str) -> None:
        if self.status != SequenceStatus.ACTIVE:
            raise ValueError("Sequence must be active to stop.")
        self.status = SequenceStatus.STOPPED
        self.stop_reason = reason
        self.ended_at = datetime.now(UTC)
        self.touch()

    # ---------------------------------------------------------
    # Wait-time rules
    # ---------------------------------------------------------

    def next_touch_due_at(self) -> datetime | None:
        """When the next pending touch is due, or None if not active or exhausted.

        Each touch's wait_days is relative to the previous touch (or to
        started_at for the first touch); this sums cumulatively up to and
        including the next pending touch.
        """
        if self.status != SequenceStatus.ACTIVE or self.current_touch_index >= len(self.touches):
            return None

        cumulative_days = sum(touch.wait_days for touch in self.touches[: self.current_touch_index + 1])
        return self.started_at + timedelta(days=cumulative_days)
