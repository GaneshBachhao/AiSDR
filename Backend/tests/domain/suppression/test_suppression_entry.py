from __future__ import annotations

from app.domain.contact.value_objects.email import Email
from app.domain.suppression.entities.suppression_entry import SuppressionEntry
from app.domain.suppression.enums.suppression_reason import SuppressionReason


def test_defaults_to_manual_reason_and_now_timestamp() -> None:
    entry = SuppressionEntry(email=Email("foo@bar.com"))

    assert entry.reason is SuppressionReason.MANUAL
    assert entry.suppressed_at is not None
    assert entry.notes is None


def test_accepts_a_bounce_reason_and_notes() -> None:
    entry = SuppressionEntry(
        email=Email("foo@bar.com"),
        reason=SuppressionReason.BOUNCE,
        notes="  mailbox full  ",
    )

    assert entry.reason is SuppressionReason.BOUNCE
    assert entry.notes == "mailbox full"


def test_blank_notes_become_none() -> None:
    entry = SuppressionEntry(email=Email("foo@bar.com"), notes="   ")

    assert entry.notes is None


def test_id_defaults_to_a_generated_identifier() -> None:
    entry = SuppressionEntry(email=Email("foo@bar.com"))

    assert entry.id is not None
