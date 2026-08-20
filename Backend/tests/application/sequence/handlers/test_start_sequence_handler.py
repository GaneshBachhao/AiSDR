"""Tests for StartSequenceHandler (EPIC-09.1) -- the first real caller of
EPIC-16's review gate: Sequence.start() must be blocked unless the Lead
has been approved."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.sequence.handlers.start_sequence_handler import (
    StartSequenceHandler,
)
from app.application.sequence.sequence_commands import StartSequenceCommand
from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.lead.entities.lead import Lead
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.sequence.entities.sequence import Sequence
from app.domain.sequence.enums.sequence_status import SequenceStatus
from app.domain.sequence.enums.touch_channel import TouchChannel
from app.domain.sequence.value_objects.touch import Touch


def _sequence(lead_id: LeadId) -> Sequence:
    return Sequence(lead_id=lead_id, touches=[Touch(channel=TouchChannel.EMAIL, wait_days=0)])


def _approved_lead(lead_id: LeadId) -> Lead:
    lead = Lead(id=lead_id, company_id=CompanyId(), contact_id=ContactId())
    lead.submit_for_review()
    lead.approve()
    return lead


def _not_submitted_lead(lead_id: LeadId) -> Lead:
    return Lead(id=lead_id, company_id=CompanyId(), contact_id=ContactId())


@pytest.fixture
def unit_of_work():
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False
    return uow


@pytest.fixture
def handler(unit_of_work):
    return StartSequenceHandler(unit_of_work=unit_of_work)


@pytest.mark.asyncio
async def test_starts_when_the_lead_is_approved(handler, unit_of_work):
    lead_id = LeadId()
    sequence = _sequence(lead_id)
    unit_of_work.sequence_repository.get_by_id.return_value = sequence
    unit_of_work.lead_repository.get_by_id.return_value = _approved_lead(lead_id)

    result = await handler.handle(StartSequenceCommand(sequence_id=str(sequence.id)))

    assert result.status == SequenceStatus.ACTIVE
    unit_of_work.sequence_repository.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_raises_conflict_when_the_lead_is_not_approved(handler, unit_of_work):
    lead_id = LeadId()
    sequence = _sequence(lead_id)
    unit_of_work.sequence_repository.get_by_id.return_value = sequence
    unit_of_work.lead_repository.get_by_id.return_value = _not_submitted_lead(lead_id)

    with pytest.raises(ConflictException, match="approved via the review gate"):
        await handler.handle(StartSequenceCommand(sequence_id=str(sequence.id)))

    unit_of_work.sequence_repository.update.assert_not_awaited()
    assert sequence.status == SequenceStatus.DRAFT


@pytest.mark.asyncio
async def test_raises_not_found_for_an_unknown_sequence(handler, unit_of_work):
    unit_of_work.sequence_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await handler.handle(StartSequenceCommand(sequence_id=str(LeadId())))


@pytest.mark.asyncio
async def test_raises_not_found_when_the_sequences_lead_is_missing(handler, unit_of_work):
    sequence = _sequence(LeadId())
    unit_of_work.sequence_repository.get_by_id.return_value = sequence
    unit_of_work.lead_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await handler.handle(StartSequenceCommand(sequence_id=str(sequence.id)))


@pytest.mark.asyncio
async def test_raises_conflict_when_already_active(handler, unit_of_work):
    lead_id = LeadId()
    sequence = _sequence(lead_id)
    sequence.start()
    unit_of_work.sequence_repository.get_by_id.return_value = sequence
    unit_of_work.lead_repository.get_by_id.return_value = _approved_lead(lead_id)

    with pytest.raises(ConflictException, match="Draft status to start"):
        await handler.handle(StartSequenceCommand(sequence_id=str(sequence.id)))
