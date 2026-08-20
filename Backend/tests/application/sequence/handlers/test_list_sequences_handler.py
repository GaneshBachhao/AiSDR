"""Tests for ListSequencesHandler (EPIC-09.1)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.sequence.handlers.list_sequences_handler import (
    ListSequencesHandler,
)
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
    return ListSequencesHandler(unit_of_work=unit_of_work)


@pytest.mark.asyncio
async def test_lists_sequences_for_a_lead(handler, unit_of_work):
    lead_id = LeadId()
    unit_of_work.sequence_repository.list_by_lead.return_value = [
        Sequence(lead_id=lead_id, touches=[Touch(channel=TouchChannel.EMAIL, wait_days=0)]),
    ]

    result = await handler.handle(str(lead_id))

    assert len(result) == 1
    unit_of_work.sequence_repository.list_by_lead.assert_awaited_once()
