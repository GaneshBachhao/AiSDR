"""Tests for RecordSequenceBounceHandler (EPIC-09.1)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.sequence.handlers.record_sequence_bounce_handler import (
    RecordSequenceBounceHandler,
)
from app.application.sequence.sequence_commands import RecordSequenceBounceCommand
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.sequence.entities.sequence import Sequence
from app.domain.sequence.enums.sequence_status import SequenceStatus
from app.domain.sequence.enums.touch_channel import TouchChannel
from app.domain.sequence.value_objects.touch import Touch


def _active_sequence() -> Sequence:
    sequence = Sequence(lead_id=LeadId(), touches=[Touch(channel=TouchChannel.EMAIL, wait_days=0)])
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
    return RecordSequenceBounceHandler(unit_of_work=unit_of_work)


@pytest.mark.asyncio
async def test_stops_an_active_sequence_with_reason_bounced(handler, unit_of_work):
    sequence = _active_sequence()
    unit_of_work.sequence_repository.get_by_id.return_value = sequence

    result = await handler.handle(RecordSequenceBounceCommand(sequence_id=str(sequence.id)))

    assert result.status == SequenceStatus.STOPPED
    assert result.stop_reason == "bounced"


@pytest.mark.asyncio
async def test_raises_not_found_for_an_unknown_sequence(handler, unit_of_work):
    unit_of_work.sequence_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await handler.handle(RecordSequenceBounceCommand(sequence_id=str(LeadId())))


@pytest.mark.asyncio
async def test_raises_conflict_when_not_active(handler, unit_of_work):
    sequence = Sequence(lead_id=LeadId(), touches=[Touch(channel=TouchChannel.EMAIL, wait_days=0)])
    unit_of_work.sequence_repository.get_by_id.return_value = sequence

    with pytest.raises(ConflictException):
        await handler.handle(RecordSequenceBounceCommand(sequence_id=str(sequence.id)))
