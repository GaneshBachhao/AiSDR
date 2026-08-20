"""Tests for CreateSuppressionHandler (EPIC-11)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.validation_exception import ValidationException
from app.application.suppression.handlers.create_suppression_handler import (
    CreateSuppressionHandler,
)
from app.application.suppression.suppression_commands import CreateSuppressionCommand
from app.domain.contact.value_objects.email import Email
from app.domain.suppression.entities.suppression_entry import SuppressionEntry
from app.domain.suppression.enums.suppression_reason import SuppressionReason


@pytest.fixture
def unit_of_work():
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False
    return uow


@pytest.fixture
def handler(unit_of_work):
    return CreateSuppressionHandler(unit_of_work=unit_of_work)


@pytest.mark.asyncio
async def test_creates_a_new_suppression_entry(handler, unit_of_work):
    unit_of_work.suppression_repository.find_by_email.return_value = None

    result = await handler.handle(
        CreateSuppressionCommand(email="foo@bar.com", reason=SuppressionReason.MANUAL, notes="opted out")
    )

    assert result.email == "foo@bar.com"
    assert result.reason == SuppressionReason.MANUAL
    unit_of_work.suppression_repository.add.assert_awaited_once()


@pytest.mark.asyncio
async def test_is_idempotent_for_an_already_suppressed_email(handler, unit_of_work):
    existing = SuppressionEntry(email=Email("foo@bar.com"), reason=SuppressionReason.BOUNCE)
    unit_of_work.suppression_repository.find_by_email.return_value = existing

    result = await handler.handle(CreateSuppressionCommand(email="foo@bar.com"))

    assert result.reason == SuppressionReason.BOUNCE
    unit_of_work.suppression_repository.add.assert_not_awaited()


@pytest.mark.asyncio
async def test_raises_validation_exception_for_a_malformed_email(handler, unit_of_work):
    with pytest.raises(ValidationException):
        await handler.handle(CreateSuppressionCommand(email="not-an-email"))
