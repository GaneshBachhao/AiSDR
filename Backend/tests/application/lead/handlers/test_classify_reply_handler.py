"""Tests for ClassifyReplyHandler (EPIC-10.1/10.3)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.lead.handlers.classify_reply_handler import ClassifyReplyHandler
from app.application.lead.lead_commands import ClassifyReplyCommand
from app.application.lead.ports.reply_classification_port import ReplyClassificationResult
from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.lead.entities.lead import Lead
from app.domain.lead.enums.lead_status import LeadStatus
from app.domain.lead.enums.reply_classification import ReplyClassification
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.lead.value_objects.lead_score import LeadScore
from app.domain.sequence.entities.sequence import Sequence
from app.domain.sequence.enums.sequence_status import SequenceStatus
from app.domain.sequence.enums.touch_channel import TouchChannel
from app.domain.sequence.value_objects.touch import Touch


def _lead(lead_id: LeadId, score: int = 50) -> Lead:
    return Lead(id=lead_id, company_id=CompanyId(), contact_id=ContactId(), score=LeadScore(score))


def _active_sequence(lead_id: LeadId) -> Sequence:
    sequence = Sequence(lead_id=lead_id, touches=[Touch(channel=TouchChannel.EMAIL, wait_days=0)])
    sequence.start()
    return sequence


@pytest.fixture
def unit_of_work():
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False
    uow.sequence_repository.list_by_lead.return_value = []
    return uow


@pytest.fixture
def budget_port():
    return AsyncMock()


@pytest.fixture
def reply_classification_port():
    return AsyncMock()


@pytest.fixture
def handler(unit_of_work, budget_port, reply_classification_port):
    return ClassifyReplyHandler(
        unit_of_work=unit_of_work,
        budget_port=budget_port,
        reply_classification_port=reply_classification_port,
    )


@pytest.mark.asyncio
async def test_raises_not_found_for_an_unknown_lead(handler, unit_of_work):
    unit_of_work.lead_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await handler.handle(ClassifyReplyCommand(lead_id=str(LeadId()), reply_text="hi"))


@pytest.mark.asyncio
async def test_checks_budget_for_a_single_call(handler, unit_of_work, budget_port, reply_classification_port):
    lead_id = LeadId()
    unit_of_work.lead_repository.get_by_id.return_value = _lead(lead_id)
    reply_classification_port.classify.return_value = ReplyClassificationResult(
        classification=ReplyClassification.NOT_NOW, confidence="HIGH"
    )

    await handler.handle(ClassifyReplyCommand(lead_id=str(lead_id), reply_text="Not right now."))

    budget_port.ensure_batch_fits.assert_awaited_once_with("gemini", 1)


@pytest.mark.asyncio
async def test_interested_qualifies_lead_and_boosts_score(handler, unit_of_work, reply_classification_port):
    lead_id = LeadId()
    unit_of_work.lead_repository.get_by_id.return_value = _lead(lead_id, score=50)
    reply_classification_port.classify.return_value = ReplyClassificationResult(
        classification=ReplyClassification.INTERESTED, confidence="HIGH"
    )

    result = await handler.handle(ClassifyReplyCommand(lead_id=str(lead_id), reply_text="Let's talk!"))

    assert result.lead_status == LeadStatus.QUALIFIED.value
    assert result.lead_score == 70
    unit_of_work.lead_repository.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_interested_score_boost_is_capped_at_100(handler, unit_of_work, reply_classification_port):
    lead_id = LeadId()
    unit_of_work.lead_repository.get_by_id.return_value = _lead(lead_id, score=90)
    reply_classification_port.classify.return_value = ReplyClassificationResult(
        classification=ReplyClassification.INTERESTED, confidence="HIGH"
    )

    result = await handler.handle(ClassifyReplyCommand(lead_id=str(lead_id), reply_text="Let's talk!"))

    assert result.lead_score == 100


@pytest.mark.asyncio
async def test_not_now_moves_to_contacted_and_nudges_score_down(
    handler, unit_of_work, reply_classification_port
):
    lead_id = LeadId()
    unit_of_work.lead_repository.get_by_id.return_value = _lead(lead_id, score=10)
    reply_classification_port.classify.return_value = ReplyClassificationResult(
        classification=ReplyClassification.NOT_NOW, confidence="MEDIUM"
    )

    result = await handler.handle(ClassifyReplyCommand(lead_id=str(lead_id), reply_text="Maybe later."))

    assert result.lead_status == LeadStatus.CONTACTED.value
    assert result.lead_score == 5


@pytest.mark.asyncio
async def test_not_now_score_floor_is_zero(handler, unit_of_work, reply_classification_port):
    lead_id = LeadId()
    unit_of_work.lead_repository.get_by_id.return_value = _lead(lead_id, score=2)
    reply_classification_port.classify.return_value = ReplyClassificationResult(
        classification=ReplyClassification.NOT_NOW, confidence="MEDIUM"
    )

    result = await handler.handle(ClassifyReplyCommand(lead_id=str(lead_id), reply_text="Maybe later."))

    assert result.lead_score == 0


@pytest.mark.asyncio
async def test_objection_moves_to_contacted_without_score_change(
    handler, unit_of_work, reply_classification_port
):
    lead_id = LeadId()
    unit_of_work.lead_repository.get_by_id.return_value = _lead(lead_id, score=50)
    reply_classification_port.classify.return_value = ReplyClassificationResult(
        classification=ReplyClassification.OBJECTION, confidence="MEDIUM"
    )

    result = await handler.handle(ClassifyReplyCommand(lead_id=str(lead_id), reply_text="Too expensive."))

    assert result.lead_status == LeadStatus.CONTACTED.value
    assert result.lead_score == 50


@pytest.mark.asyncio
async def test_unsubscribe_disqualifies_lead(handler, unit_of_work, reply_classification_port):
    lead_id = LeadId()
    unit_of_work.lead_repository.get_by_id.return_value = _lead(lead_id)
    reply_classification_port.classify.return_value = ReplyClassificationResult(
        classification=ReplyClassification.UNSUBSCRIBE, confidence="HIGH"
    )

    result = await handler.handle(ClassifyReplyCommand(lead_id=str(lead_id), reply_text="Unsubscribe me."))

    assert result.lead_status == LeadStatus.DISQUALIFIED.value


@pytest.mark.asyncio
async def test_wrong_person_disqualifies_lead(handler, unit_of_work, reply_classification_port):
    lead_id = LeadId()
    unit_of_work.lead_repository.get_by_id.return_value = _lead(lead_id)
    reply_classification_port.classify.return_value = ReplyClassificationResult(
        classification=ReplyClassification.WRONG_PERSON, confidence="HIGH"
    )

    result = await handler.handle(ClassifyReplyCommand(lead_id=str(lead_id), reply_text="Wrong department."))

    assert result.lead_status == LeadStatus.DISQUALIFIED.value


@pytest.mark.asyncio
async def test_out_of_office_changes_nothing_and_does_not_stop_sequence(
    handler, unit_of_work, reply_classification_port
):
    lead_id = LeadId()
    lead = _lead(lead_id, score=50)
    unit_of_work.lead_repository.get_by_id.return_value = lead
    sequence = _active_sequence(lead_id)
    unit_of_work.sequence_repository.list_by_lead.return_value = [sequence]
    reply_classification_port.classify.return_value = ReplyClassificationResult(
        classification=ReplyClassification.OUT_OF_OFFICE, confidence="HIGH"
    )

    result = await handler.handle(ClassifyReplyCommand(lead_id=str(lead_id), reply_text="Out of office."))

    assert result.lead_status == LeadStatus.NEW.value
    assert result.lead_score == 50
    assert result.sequences_stopped == []
    assert sequence.status == SequenceStatus.ACTIVE


@pytest.mark.asyncio
async def test_real_reply_stops_all_active_sequences_for_the_lead(
    handler, unit_of_work, reply_classification_port
):
    lead_id = LeadId()
    unit_of_work.lead_repository.get_by_id.return_value = _lead(lead_id)
    active_one = _active_sequence(lead_id)
    active_two = _active_sequence(lead_id)
    draft = Sequence(lead_id=lead_id, touches=[Touch(channel=TouchChannel.EMAIL, wait_days=0)])
    unit_of_work.sequence_repository.list_by_lead.return_value = [active_one, active_two, draft]
    reply_classification_port.classify.return_value = ReplyClassificationResult(
        classification=ReplyClassification.NOT_NOW, confidence="HIGH"
    )

    result = await handler.handle(ClassifyReplyCommand(lead_id=str(lead_id), reply_text="Not now."))

    assert active_one.status == SequenceStatus.STOPPED
    assert active_two.status == SequenceStatus.STOPPED
    assert draft.status == SequenceStatus.DRAFT
    assert sorted(result.sequences_stopped) == sorted([str(active_one.id), str(active_two.id)])
    assert unit_of_work.sequence_repository.update.await_count == 2


@pytest.mark.asyncio
async def test_no_active_sequences_does_not_error(handler, unit_of_work, reply_classification_port):
    lead_id = LeadId()
    unit_of_work.lead_repository.get_by_id.return_value = _lead(lead_id)
    unit_of_work.sequence_repository.list_by_lead.return_value = []
    reply_classification_port.classify.return_value = ReplyClassificationResult(
        classification=ReplyClassification.INTERESTED, confidence="HIGH"
    )

    result = await handler.handle(ClassifyReplyCommand(lead_id=str(lead_id), reply_text="Yes!"))

    assert result.sequences_stopped == []
