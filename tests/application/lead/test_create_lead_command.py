# tests/application/lead/test_create_lead_command.py

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.application.lead.commands.create_lead import (
    CreateLeadCommand,
)


def test_create_lead_command_accepts_valid_data() -> None:

    command = CreateLeadCommand(
        company_name="Pamacore Labs",
        contact_name="Ganesh",
        email="contact@pamacore.com",
    )

    assert command.company_name == "Pamacore Labs"
    assert command.contact_name == "Ganesh"


def test_create_lead_command_rejects_unknown_fields() -> None:

    with pytest.raises(ValidationError):

        CreateLeadCommand(
            company_name="Pamacore",
            contact_name="Test",
            email="test@test.com",
            invalid="value",
        )


def test_create_lead_command_is_immutable() -> None:

    command = CreateLeadCommand(
        company_name="Pamacore",
        contact_name="Test",
        email="test@test.com",
    )

    with pytest.raises(ValidationError):

        command.company_name = "Changed"