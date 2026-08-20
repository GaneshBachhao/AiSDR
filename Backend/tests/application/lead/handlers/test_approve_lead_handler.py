"""Tests for ApproveLeadHandler (EPIC-16)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.lead.handlers.approve_lead_handler import ApproveLeadHandler
from app.application.lead.lead_commands import ApproveLeadCommand
from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.lead.entities.lead import Lead
from app.domain.lead.enums.lead_review_status import LeadReviewStatus


def _pending_lead() -> Lead:
    lead = Lead(company_id=CompanyId(), contact_id=ContactId())
    lead.submit_for_review()
    return lead


@pytest.fixture
def unit_of_work():
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False
    return uow


@pytest.fixture
def handler(unit_of_work):
    return ApproveLeadHandler(unit_of_work=unit_of_work)


@pytest.mark.asyncio
async def test_approve_moves_a_pending_review_lead_to_approved(handler, unit_of_work):
    lead = _pending_lead()
    unit_of_work.lead_repository.get_by_id.return_value = lead

    result = await handler.handle(ApproveLeadCommand(lead_id=str(lead.id), notes="Looks solid."))

    assert result.review_status == LeadReviewStatus.APPROVED
    assert result.review_notes == "Looks solid."
    unit_of_work.lead_repository.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_approve_raises_not_found_for_an_unknown_lead(handler, unit_of_work):
    unit_of_work.lead_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await handler.handle(ApproveLeadCommand(lead_id=str(CompanyId())))


@pytest.mark.asyncio
async def test_approve_raises_conflict_when_not_pending_review(handler, unit_of_work):
    lead = Lead(company_id=CompanyId(), contact_id=ContactId())
    unit_of_work.lead_repository.get_by_id.return_value = lead

    with pytest.raises(ConflictException):
        await handler.handle(ApproveLeadCommand(lead_id=str(lead.id)))

    unit_of_work.lead_repository.update.assert_not_awaited()
