"""
Touch — one planned step in a Sequence.

Immutable and identity-less: a Touch is a plan line-item owned entirely by
its Sequence, set once at creation and never mutated afterward (only the
owning Sequence's own progress fields change as touches actually happen).
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.sequence.enums.touch_channel import TouchChannel


@dataclass(frozen=True, slots=True)
class Touch:
    """One planned touch: a channel and how many days to wait before it fires.

    ``wait_days`` is relative to the *previous* touch (or to the
    Sequence's ``started_at`` for the first touch) -- Sequence.
    next_touch_due_at() sums these cumulatively.
    """

    channel: TouchChannel
    wait_days: int

    def __post_init__(self) -> None:
        if self.wait_days < 0:
            raise ValueError("wait_days cannot be negative.")
