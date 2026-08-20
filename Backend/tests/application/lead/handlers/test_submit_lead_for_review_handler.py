"""Tests for SubmitLeadForReviewHandler (EPIC-16)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.lead.handlers.submit_lead_for_review_handler import (
    SubmitLeadForReviewHandler,
)
from app.application.lead.lead_commands import SubmitLeadForReviewCommand
from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.lead.entities.lead import Lead
from app.domain.lead.enums.lead_review_status import LeadReviewStatus


def _lead() -> Lead:
    return Lead(company_id=CompanyId(), contact_id=ContactId())


@pytest.fixture
def unit_of_work():
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False
    return uow


@pytest.fixture
def handler(unit_of_work):
    return SubmitLeadForReviewHandler(unit_of_work=unit_of_work)


@pytest.mark.asyncio
async def test_submit_moves_a_not_submitted_lead_to_pending_review(handler, unit_of_work):
    lead = _lead()
    unit_of_work.lead_repository.get_by_id.return_value = lead

    result = await handler.handle(SubmitLeadForReviewCommand(lead_id=str(lead.id)))

    assert result.review_status == LeadReviewStatus.PENDING_REVIEW
    unit_of_work.lead_repository.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_submit_raises_not_found_for_an_unknown_lead(handler, unit_of_work):
    unit_of_work.lead_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await handler.handle(SubmitLeadForReviewCommand(lead_id=str(CompanyId())))


@pytest.mark.asyncio
async def test_submit_raises_conflict_when_already_approved(handler, unit_of_work):
    lead = _lead()
    lead.submit_for_review()
    lead.approve()
    unit_of_work.lead_repository.get_by_id.return_value = lead

    with pytest.raises(ConflictException):
        await handler.handle(SubmitLeadForReviewCommand(lead_id=str(lead.id)))

    unit_of_work.lead_repository.update.assert_not_awaited()
