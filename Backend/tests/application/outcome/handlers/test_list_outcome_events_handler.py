"""Tests for ListOutcomeEventsHandler (EPIC-12)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.outcome.handlers.list_outcome_events_handler import (
    ListOutcomeEventsHandler,
)
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.outcome.entities.outcome_event import OutcomeEvent
from app.domain.outcome.enums.outcome_type import OutcomeType


@pytest.fixture
def unit_of_work():
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False
    return uow


@pytest.fixture
def handler(unit_of_work):
    return ListOutcomeEventsHandler(unit_of_work=unit_of_work)


@pytest.mark.asyncio
async def test_lists_all_events_when_no_lead_id_given(handler, unit_of_work):
    unit_of_work.outcome_repository.list.return_value = [
        OutcomeEvent(lead_id=LeadId(), outcome_type=OutcomeType.WON),
    ]

    result = await handler.handle()

    assert len(result) == 1
    unit_of_work.outcome_repository.list_by_lead.assert_not_awaited()


@pytest.mark.asyncio
async def test_lists_events_for_one_lead_when_lead_id_given(handler, unit_of_work):
    lead_id = LeadId()
    unit_of_work.outcome_repository.list_by_lead.return_value = [
        OutcomeEvent(lead_id=lead_id, outcome_type=OutcomeType.LOST),
    ]

    result = await handler.handle(lead_id=str(lead_id))

    assert len(result) == 1
    unit_of_work.outcome_repository.list.assert_not_awaited()
