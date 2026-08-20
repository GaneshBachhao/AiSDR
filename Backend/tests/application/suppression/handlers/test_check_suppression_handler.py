"""Tests for CheckSuppressionHandler (EPIC-11)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.validation_exception import ValidationException
from app.application.suppression.handlers.check_suppression_handler import (
    CheckSuppressionHandler,
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
    return CheckSuppressionHandler(unit_of_work=unit_of_work)


@pytest.mark.asyncio
async def test_reports_suppressed_true_with_the_entry(handler, unit_of_work):
    entry = SuppressionEntry(email=Email("foo@bar.com"))
    unit_of_work.suppression_repository.find_by_email.return_value = entry

    result = await handler.handle("foo@bar.com")

    assert result.suppressed is True
    assert result.entry is not None
    assert result.entry.email == "foo@bar.com"


@pytest.mark.asyncio
async def test_reports_suppressed_false_with_no_entry(handler, unit_of_work):
    unit_of_work.suppression_repository.find_by_email.return_value = None

    result = await handler.handle("clean@bar.com")

    assert result.suppressed is False
    assert result.entry is None


@pytest.mark.asyncio
async def test_raises_validation_exception_for_a_malformed_email(handler, unit_of_work):
    with pytest.raises(ValidationException):
        await handler.handle("not-an-email")
