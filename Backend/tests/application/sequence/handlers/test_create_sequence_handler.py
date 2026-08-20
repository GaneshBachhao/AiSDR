"""Tests for CreateSequenceHandler (EPIC-09.1)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.exceptions.validation_exception import ValidationException
from app.application.sequence.handlers.create_sequence_handler import (
    CreateSequenceHandler,
)
from app.application.sequence.sequence_commands import CreateSequenceCommand, TouchInput
from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.lead.entities.lead import Lead
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.sequence.enums.touch_channel import TouchChannel


def _lead() -> Lead:
    return Lead(company_id=CompanyId(), contact_id=ContactId())


def _command(**overrides) -> CreateSequenceCommand:
    defaults = dict(
        lead_id=str(LeadId()),
        touches=[TouchInput(channel=TouchChannel.EMAIL, wait_days=0)],
    )
    defaults.update(overrides)
    return CreateSequenceCommand(**defaults)


@pytest.fixture
def unit_of_work():
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False
    return uow


@pytest.fixture
def handler(unit_of_work):
    return CreateSequenceHandler(unit_of_work=unit_of_work)


@pytest.mark.asyncio
async def test_creates_a_sequence_for_an_existing_lead(handler, unit_of_work):
    unit_of_work.lead_repository.get_by_id.return_value = _lead()

    result = await handler.handle(_command())

    assert len(result.touches) == 1
    unit_of_work.sequence_repository.add.assert_awaited_once()


@pytest.mark.asyncio
async def test_raises_not_found_for_an_unknown_lead(handler, unit_of_work):
    unit_of_work.lead_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await handler.handle(_command())

    unit_of_work.sequence_repository.add.assert_not_awaited()


@pytest.mark.asyncio
async def test_raises_validation_exception_for_no_touches(handler, unit_of_work):
    with pytest.raises(ValidationException):
        await handler.handle(_command(touches=[]))

    unit_of_work.lead_repository.get_by_id.assert_not_awaited()
