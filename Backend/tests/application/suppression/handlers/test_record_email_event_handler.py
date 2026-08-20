"""Tests for RecordEmailEventHandler (EPIC-11, bounce/complaint webhook)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.validation_exception import ValidationException
from app.application.suppression.handlers.record_email_event_handler import (
    RecordEmailEventHandler,
)
from app.application.suppression.suppression_commands import RecordEmailEventCommand
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
    return RecordEmailEventHandler(unit_of_work=unit_of_work)


@pytest.mark.asyncio
async def test_bounce_event_creates_a_suppression_with_bounce_reason(handler, unit_of_work):
    unit_of_work.suppression_repository.find_by_email.return_value = None

    result = await handler.handle(
        RecordEmailEventCommand(email="bounced@example.com", event_type="bounce", reason="mailbox_full")
    )

    assert result.reason == SuppressionReason.BOUNCE
    unit_of_work.suppression_repository.add.assert_awaited_once()


@pytest.mark.asyncio
async def test_complaint_event_creates_a_suppression_with_complaint_reason(handler, unit_of_work):
    unit_of_work.suppression_repository.find_by_email.return_value = None

    result = await handler.handle(
        RecordEmailEventCommand(email="complained@example.com", event_type="complaint")
    )

    assert result.reason == SuppressionReason.COMPLAINT


@pytest.mark.asyncio
async def test_is_idempotent_for_an_already_suppressed_email(handler, unit_of_work):
    existing = SuppressionEntry(email=Email("already@example.com"), reason=SuppressionReason.MANUAL)
    unit_of_work.suppression_repository.find_by_email.return_value = existing

    result = await handler.handle(RecordEmailEventCommand(email="already@example.com", event_type="bounce"))

    assert result.reason == SuppressionReason.MANUAL
    unit_of_work.suppression_repository.add.assert_not_awaited()


@pytest.mark.asyncio
async def test_raises_validation_exception_for_an_unknown_event_type(handler, unit_of_work):
    with pytest.raises(ValidationException):
        await handler.handle(RecordEmailEventCommand(email="foo@bar.com", event_type="unsubscribe"))


@pytest.mark.asyncio
async def test_raises_validation_exception_for_a_malformed_email(handler, unit_of_work):
    with pytest.raises(ValidationException):
        await handler.handle(RecordEmailEventCommand(email="not-an-email", event_type="bounce"))
