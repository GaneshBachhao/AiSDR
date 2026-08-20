"""Tests for DeleteSuppressionHandler (EPIC-11)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.suppression.handlers.delete_suppression_handler import (
    DeleteSuppressionHandler,
)
from app.application.suppression.suppression_commands import DeleteSuppressionCommand
from app.domain.suppression.identifiers.suppression_entry_id import SuppressionEntryId


@pytest.fixture
def unit_of_work():
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False
    return uow


@pytest.fixture
def handler(unit_of_work):
    return DeleteSuppressionHandler(unit_of_work=unit_of_work)


@pytest.mark.asyncio
async def test_deletes_an_existing_suppression(handler, unit_of_work):
    unit_of_work.suppression_repository.exists.return_value = True
    entry_id = str(SuppressionEntryId())

    await handler.handle(DeleteSuppressionCommand(suppression_id=entry_id))

    unit_of_work.suppression_repository.delete.assert_awaited_once()


@pytest.mark.asyncio
async def test_raises_not_found_for_an_unknown_entry(handler, unit_of_work):
    unit_of_work.suppression_repository.exists.return_value = False

    with pytest.raises(NotFoundException):
        await handler.handle(DeleteSuppressionCommand(suppression_id=str(SuppressionEntryId())))

    unit_of_work.suppression_repository.delete.assert_not_awaited()
