from __future__ import annotations

import pytest

from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.sequence.entities.sequence import Sequence
from app.domain.sequence.enums.sequence_status import SequenceStatus
from app.domain.sequence.enums.touch_channel import TouchChannel
from app.domain.sequence.value_objects.touch import Touch


def _three_touch_plan() -> list[Touch]:
    return [
        Touch(channel=TouchChannel.EMAIL, wait_days=0),
        Touch(channel=TouchChannel.LINKEDIN, wait_days=3),
        Touch(channel=TouchChannel.EMAIL, wait_days=4),
    ]


def _sequence(**overrides) -> Sequence:
    defaults = dict(lead_id=LeadId(), touches=_three_touch_plan())
    defaults.update(overrides)
    return Sequence(**defaults)


def test_requires_at_least_one_touch() -> None:
    with pytest.raises(ValueError, match="at least one touch"):
        Sequence(lead_id=LeadId(), touches=[])


def test_defaults_to_draft() -> None:
    sequence = _sequence()

    assert sequence.status is SequenceStatus.DRAFT
    assert sequence.current_touch_index == 0
    assert sequence.started_at is None


def test_start_moves_to_active_and_stamps_started_at() -> None:
    sequence = _sequence()

    sequence.start()

    assert sequence.status is SequenceStatus.ACTIVE
    assert sequence.started_at is not None


def test_start_twice_raises() -> None:
    sequence = _sequence()
    sequence.start()

    with pytest.raises(ValueError, match="Draft status to start"):
        sequence.start()


def test_advance_before_start_raises() -> None:
    sequence = _sequence()

    with pytest.raises(ValueError, match="must be active to advance"):
        sequence.advance()


def test_advance_moves_through_touches_and_completes_naturally() -> None:
    sequence = _sequence()
    sequence.start()

    sequence.advance()
    assert sequence.current_touch_index == 1
    assert sequence.status is SequenceStatus.ACTIVE

    sequence.advance()
    assert sequence.current_touch_index == 2
    assert sequence.status is SequenceStatus.ACTIVE

    sequence.advance()
    assert sequence.current_touch_index == 3
    assert sequence.status is SequenceStatus.COMPLETED
    assert sequence.ended_at is not None


def test_advance_after_completion_raises() -> None:
    sequence = _sequence(touches=[Touch(channel=TouchChannel.EMAIL, wait_days=0)])
    sequence.start()
    sequence.advance()  # exhausts the single-touch plan -> COMPLETED

    with pytest.raises(ValueError, match="must be active to advance"):
        sequence.advance()


def test_record_reply_stops_the_sequence() -> None:
    sequence = _sequence()
    sequence.start()

    sequence.record_reply()

    assert sequence.status is SequenceStatus.STOPPED
    assert sequence.stop_reason == "replied"
    assert sequence.ended_at is not None


def test_record_bounce_stops_the_sequence() -> None:
    sequence = _sequence()
    sequence.start()

    sequence.record_bounce()

    assert sequence.status is SequenceStatus.STOPPED
    assert sequence.stop_reason == "bounced"


def test_record_reply_before_start_raises() -> None:
    sequence = _sequence()

    with pytest.raises(ValueError, match="must be active to stop"):
        sequence.record_reply()


def test_record_reply_after_stopped_raises() -> None:
    sequence = _sequence()
    sequence.start()
    sequence.record_bounce()

    with pytest.raises(ValueError, match="must be active to stop"):
        sequence.record_reply()


def test_next_touch_due_at_is_none_before_start() -> None:
    sequence = _sequence()

    assert sequence.next_touch_due_at() is None


def test_next_touch_due_at_sums_wait_days_cumulatively() -> None:
    sequence = _sequence()
    sequence.start()

    first_due = sequence.next_touch_due_at()
    assert first_due == sequence.started_at  # touch 0: wait_days=0

    sequence.advance()
    second_due = sequence.next_touch_due_at()
    assert (second_due - sequence.started_at).days == 3  # touch 1: wait_days=3

    sequence.advance()
    third_due = sequence.next_touch_due_at()
    assert (third_due - sequence.started_at).days == 7  # touch 2: +4 = 7 total


def test_next_touch_due_at_is_none_once_exhausted() -> None:
    sequence = _sequence(touches=[Touch(channel=TouchChannel.EMAIL, wait_days=0)])
    sequence.start()
    sequence.advance()

    assert sequence.next_touch_due_at() is None


def test_next_touch_due_at_is_none_once_stopped() -> None:
    sequence = _sequence()
    sequence.start()
    sequence.record_reply()

    assert sequence.next_touch_due_at() is None
