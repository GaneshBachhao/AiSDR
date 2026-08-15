from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.application.lead.lead_commands import CreateLeadCommand

COMPANY_ID = "00000000-0000-0000-0000-000000000001"
CONTACT_ID = "00000000-0000-0000-0000-000000000002"


def test_create_lead_command_accepts_valid_data() -> None:
    command = CreateLeadCommand(
        company_id=COMPANY_ID,
        contact_id=CONTACT_ID,
        source="Web",
        score=20,
        notes="Initial prospect",
    )
    assert command.company_id == COMPANY_ID
    assert command.contact_id == CONTACT_ID
    assert command.source == "Web"
    assert command.score == 20
    assert command.notes == "Initial prospect"


def test_optional_fields_default_to_expected_values() -> None:
    command = CreateLeadCommand(
        company_id=COMPANY_ID,
        contact_id=CONTACT_ID,
    )
    assert command.source == "Other"
    assert command.score == 0
    assert command.notes is None


def test_create_lead_command_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        CreateLeadCommand(
            company_id=COMPANY_ID,
            contact_id=CONTACT_ID,
            invalid="value",
        )


def test_create_lead_command_is_immutable() -> None:
    command = CreateLeadCommand(
        company_id=COMPANY_ID,
        contact_id=CONTACT_ID,
    )
    with pytest.raises(ValidationError):
        command.company_id = CONTACT_ID
