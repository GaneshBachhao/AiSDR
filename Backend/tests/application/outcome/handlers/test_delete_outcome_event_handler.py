"""Tests for DeleteOutcomeEventHandler (EPIC-12)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.outcome.handlers.delete_outcome_event_handler import (
    DeleteOutcomeEventHandler,
)
from app.application.outcome.outcome_commands import DeleteOutcomeEventCommand
from app.domain.outcome.identifiers.outcome_event_id import OutcomeEventId


@pytest.fixture
def unit_of_work():
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False
    return uow


@pytest.fixture
def handler(unit_of_work):
    return DeleteOutcomeEventHandler(unit_of_work=unit_of_work)


@pytest.mark.asyncio
async def test_deletes_an_existing_outcome_event(handler, unit_of_work):
    unit_of_work.outcome_repository.exists.return_value = True

    await handler.handle(DeleteOutcomeEventCommand(outcome_id=str(OutcomeEventId())))

    unit_of_work.outcome_repository.delete.assert_awaited_once()


@pytest.mark.asyncio
async def test_raises_not_found_for_an_unknown_outcome_event(handler, unit_of_work):
    unit_of_work.outcome_repository.exists.return_value = False

    with pytest.raises(NotFoundException):
        await handler.handle(DeleteOutcomeEventCommand(outcome_id=str(OutcomeEventId())))

    unit_of_work.outcome_repository.delete.assert_not_awaited()
