"""Tests for GenerateSequenceContentHandler (EPIC-09.2)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.exceptions.validation_exception import ValidationException
from app.application.sequence.handlers.generate_sequence_content_handler import (
    GenerateSequenceContentHandler,
)
from app.application.sequence.sequence_commands import GenerateSequenceContentCommand
from app.domain.ai.entities.ai_response import AIResponse
from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.lead.entities.lead import Lead
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.sequence.entities.sequence import Sequence
from app.domain.sequence.enums.touch_channel import TouchChannel
from app.domain.sequence.value_objects.touch import Touch


def _lead_with_evidence(lead_id: LeadId) -> Lead:
    return Lead(
        id=lead_id,
        company_id=CompanyId(),
        contact_id=ContactId(),
        notes="AI-research-sourced lead. Hypothesis: manual reporting workflows.",
    )


def _lead_without_evidence(lead_id: LeadId) -> Lead:
    return Lead(id=lead_id, company_id=CompanyId(), contact_id=ContactId())


def _sequence(lead_id: LeadId, touch_count: int = 2) -> Sequence:
    touches = [Touch(channel=TouchChannel.EMAIL, wait_days=i * 3) for i in range(touch_count)]
    return Sequence(lead_id=lead_id, touches=touches)


@pytest.fixture
def unit_of_work():
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False
    uow.discovery_repository.get_by_lead.return_value = None
    uow.assessment_repository.get_by_lead_id.return_value = None
    return uow


@pytest.fixture
def ai_execution_service():
    service = AsyncMock()
    service.execute.return_value = AIResponse(content="Generated touch content.")
    return service


@pytest.fixture
def budget_port():
    return AsyncMock()


@pytest.fixture
def handler(unit_of_work, ai_execution_service, budget_port):
    return GenerateSequenceContentHandler(
        unit_of_work=unit_of_work,
        ai_execution_service=ai_execution_service,
        budget_port=budget_port,
    )


@pytest.mark.asyncio
async def test_generates_content_for_every_touch(handler, unit_of_work, ai_execution_service):
    lead_id = LeadId()
    sequence = _sequence(lead_id, touch_count=3)
    unit_of_work.sequence_repository.get_by_id.return_value = sequence
    unit_of_work.lead_repository.get_by_id.return_value = _lead_with_evidence(lead_id)

    result = await handler.handle(GenerateSequenceContentCommand(sequence_id=str(sequence.id)))

    assert all(touch.content is not None for touch in result.touches)
    assert ai_execution_service.execute.await_count == 3
    unit_of_work.sequence_repository.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_checks_budget_for_the_whole_batch(handler, unit_of_work, budget_port):
    lead_id = LeadId()
    sequence = _sequence(lead_id, touch_count=3)
    unit_of_work.sequence_repository.get_by_id.return_value = sequence
    unit_of_work.lead_repository.get_by_id.return_value = _lead_with_evidence(lead_id)

    await handler.handle(GenerateSequenceContentCommand(sequence_id=str(sequence.id)))

    budget_port.ensure_batch_fits.assert_awaited_once_with("gemini", 3)


@pytest.mark.asyncio
async def test_raises_not_found_for_an_unknown_sequence(handler, unit_of_work):
    unit_of_work.sequence_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await handler.handle(GenerateSequenceContentCommand(sequence_id=str(LeadId())))


@pytest.mark.asyncio
async def test_raises_not_found_when_the_sequences_lead_is_missing(handler, unit_of_work):
    sequence = _sequence(LeadId())
    unit_of_work.sequence_repository.get_by_id.return_value = sequence
    unit_of_work.lead_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await handler.handle(GenerateSequenceContentCommand(sequence_id=str(sequence.id)))


@pytest.mark.asyncio
async def test_raises_conflict_when_sequence_is_not_draft(handler, unit_of_work):
    lead_id = LeadId()
    sequence = _sequence(lead_id)
    unit_of_work.lead_repository.get_by_id.return_value = _lead_with_evidence(lead_id)
    sequence.start()
    unit_of_work.sequence_repository.get_by_id.return_value = sequence

    with pytest.raises(ConflictException, match="Draft status"):
        await handler.handle(GenerateSequenceContentCommand(sequence_id=str(sequence.id)))


@pytest.mark.asyncio
async def test_raises_validation_exception_when_lead_has_no_evidence(
    handler, unit_of_work, ai_execution_service
):
    lead_id = LeadId()
    sequence = _sequence(lead_id)
    unit_of_work.sequence_repository.get_by_id.return_value = sequence
    unit_of_work.lead_repository.get_by_id.return_value = _lead_without_evidence(lead_id)

    with pytest.raises(ValidationException, match="no captured evidence"):
        await handler.handle(GenerateSequenceContentCommand(sequence_id=str(sequence.id)))

    ai_execution_service.execute.assert_not_awaited()


@pytest.mark.asyncio
async def test_ai_failure_propagates_rather_than_being_swallowed(handler, unit_of_work, ai_execution_service):
    lead_id = LeadId()
    sequence = _sequence(lead_id)
    unit_of_work.sequence_repository.get_by_id.return_value = sequence
    unit_of_work.lead_repository.get_by_id.return_value = _lead_with_evidence(lead_id)
    ai_execution_service.execute.side_effect = RuntimeError("provider unavailable")

    with pytest.raises(RuntimeError, match="provider unavailable"):
        await handler.handle(GenerateSequenceContentCommand(sequence_id=str(sequence.id)))

    unit_of_work.sequence_repository.update.assert_not_awaited()
