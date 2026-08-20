"""Tests for AdvanceSequenceHandler (EPIC-09.1)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.sequence.handlers.advance_sequence_handler import (
    AdvanceSequenceHandler,
)
from app.application.sequence.sequence_commands import AdvanceSequenceCommand
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.sequence.entities.sequence import Sequence
from app.domain.sequence.enums.sequence_status import SequenceStatus
from app.domain.sequence.enums.touch_channel import TouchChannel
from app.domain.sequence.value_objects.touch import Touch


def _active_sequence() -> Sequence:
    sequence = Sequence(
        lead_id=LeadId(),
        touches=[
            Touch(channel=TouchChannel.EMAIL, wait_days=0),
            Touch(channel=TouchChannel.EMAIL, wait_days=3),
        ],
    )
    sequence.start()
    return sequence


@pytest.fixture
def unit_of_work():
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False
    return uow


@pytest.fixture
def handler(unit_of_work):
    return AdvanceSequenceHandler(unit_of_work=unit_of_work)


@pytest.mark.asyncio
async def test_advances_an_active_sequence(handler, unit_of_work):
    sequence = _active_sequence()
    unit_of_work.sequence_repository.get_by_id.return_value = sequence

    result = await handler.handle(AdvanceSequenceCommand(sequence_id=str(sequence.id)))

    assert result.current_touch_index == 1
    unit_of_work.sequence_repository.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_raises_not_found_for_an_unknown_sequence(handler, unit_of_work):
    unit_of_work.sequence_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await handler.handle(AdvanceSequenceCommand(sequence_id=str(LeadId())))


@pytest.mark.asyncio
async def test_raises_conflict_when_not_active(handler, unit_of_work):
    sequence = Sequence(lead_id=LeadId(), touches=[Touch(channel=TouchChannel.EMAIL, wait_days=0)])
    unit_of_work.sequence_repository.get_by_id.return_value = sequence

    with pytest.raises(ConflictException):
        await handler.handle(AdvanceSequenceCommand(sequence_id=str(sequence.id)))

    unit_of_work.sequence_repository.update.assert_not_awaited()


@pytest.mark.asyncio
async def test_advance_to_exhaustion_completes_the_sequence(handler, unit_of_work):
    sequence = Sequence(lead_id=LeadId(), touches=[Touch(channel=TouchChannel.EMAIL, wait_days=0)])
    sequence.start()
    unit_of_work.sequence_repository.get_by_id.return_value = sequence

    result = await handler.handle(AdvanceSequenceCommand(sequence_id=str(sequence.id)))

    assert result.status == SequenceStatus.COMPLETED
