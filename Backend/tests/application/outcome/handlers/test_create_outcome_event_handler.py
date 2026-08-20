"""Tests for CreateOutcomeEventHandler (EPIC-12)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.outcome.handlers.create_outcome_event_handler import (
    CreateOutcomeEventHandler,
)
from app.application.outcome.outcome_commands import CreateOutcomeEventCommand
from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.lead.entities.lead import Lead
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.outcome.enums.outcome_type import OutcomeType


def _lead() -> Lead:
    return Lead(company_id=CompanyId(), contact_id=ContactId())


@pytest.fixture
def unit_of_work():
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False
    return uow


@pytest.fixture
def handler(unit_of_work):
    return CreateOutcomeEventHandler(unit_of_work=unit_of_work)


@pytest.mark.asyncio
async def test_records_an_outcome_for_an_existing_lead(handler, unit_of_work):
    lead_id = LeadId()
    unit_of_work.lead_repository.get_by_id.return_value = _lead()

    result = await handler.handle(
        CreateOutcomeEventCommand(lead_id=str(lead_id), outcome_type=OutcomeType.MEETING_BOOKED)
    )

    assert result.outcome_type is OutcomeType.MEETING_BOOKED
    unit_of_work.outcome_repository.add.assert_awaited_once()


@pytest.mark.asyncio
async def test_raises_not_found_for_an_unknown_lead(handler, unit_of_work):
    unit_of_work.lead_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await handler.handle(
            CreateOutcomeEventCommand(lead_id=str(LeadId()), outcome_type=OutcomeType.NO_RESPONSE)
        )

    unit_of_work.outcome_repository.add.assert_not_awaited()


@pytest.mark.asyncio
async def test_allows_recording_multiple_outcomes_for_the_same_lead(handler, unit_of_work):
    unit_of_work.lead_repository.get_by_id.return_value = _lead()
    lead_id = str(LeadId())

    await handler.handle(CreateOutcomeEventCommand(lead_id=lead_id, outcome_type=OutcomeType.NO_RESPONSE))
    await handler.handle(CreateOutcomeEventCommand(lead_id=lead_id, outcome_type=OutcomeType.MEETING_BOOKED))

    assert unit_of_work.outcome_repository.add.await_count == 2
