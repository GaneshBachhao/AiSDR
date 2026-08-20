from __future__ import annotations

from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.outcome.entities.outcome_event import OutcomeEvent
from app.domain.outcome.enums.outcome_type import OutcomeType


def test_defaults_to_now_timestamp_and_no_notes() -> None:
    event = OutcomeEvent(lead_id=LeadId(), outcome_type=OutcomeType.NO_RESPONSE)

    assert event.occurred_at is not None
    assert event.notes is None


def test_accepts_notes() -> None:
    event = OutcomeEvent(
        lead_id=LeadId(),
        outcome_type=OutcomeType.MEETING_BOOKED,
        notes="  booked via referral  ",
    )

    assert event.notes == "booked via referral"


def test_blank_notes_become_none() -> None:
    event = OutcomeEvent(lead_id=LeadId(), outcome_type=OutcomeType.WON, notes="   ")

    assert event.notes is None


def test_id_defaults_to_a_generated_identifier() -> None:
    event = OutcomeEvent(lead_id=LeadId(), outcome_type=OutcomeType.LOST)

    assert event.id is not None
