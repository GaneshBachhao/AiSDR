"""Tests for GetSequenceHandler (EPIC-09.1)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.sequence.handlers.get_sequence_handler import GetSequenceHandler
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.sequence.entities.sequence import Sequence
from app.domain.sequence.enums.touch_channel import TouchChannel
from app.domain.sequence.value_objects.touch import Touch


@pytest.fixture
def unit_of_work():
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False
    return uow


@pytest.fixture
def handler(unit_of_work):
    return GetSequenceHandler(unit_of_work=unit_of_work)


@pytest.mark.asyncio
async def test_returns_the_sequence(handler, unit_of_work):
    sequence = Sequence(lead_id=LeadId(), touches=[Touch(channel=TouchChannel.EMAIL, wait_days=0)])
    unit_of_work.sequence_repository.get_by_id.return_value = sequence

    result = await handler.handle(str(sequence.id))

    assert result.id == str(sequence.id)


@pytest.mark.asyncio
async def test_raises_not_found_for_an_unknown_sequence(handler, unit_of_work):
    unit_of_work.sequence_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await handler.handle(str(LeadId()))
