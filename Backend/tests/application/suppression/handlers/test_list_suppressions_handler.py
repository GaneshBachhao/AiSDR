"""Tests for ListSuppressionsHandler (EPIC-11)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.suppression.handlers.list_suppressions_handler import (
    ListSuppressionsHandler,
)
from app.domain.contact.value_objects.email import Email
from app.domain.suppression.entities.suppression_entry import SuppressionEntry


@pytest.fixture
def unit_of_work():
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False
    return uow


@pytest.fixture
def handler(unit_of_work):
    return ListSuppressionsHandler(unit_of_work=unit_of_work)


@pytest.mark.asyncio
async def test_lists_all_entries(handler, unit_of_work):
    unit_of_work.suppression_repository.list.return_value = [
        SuppressionEntry(email=Email("a@example.com")),
        SuppressionEntry(email=Email("b@example.com")),
    ]

    result = await handler.handle()

    assert {entry.email for entry in result} == {"a@example.com", "b@example.com"}
