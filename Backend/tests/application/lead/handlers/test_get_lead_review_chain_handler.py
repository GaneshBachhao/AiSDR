"""Tests for GetLeadReviewChainHandler (EPIC-16)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.lead.handlers.get_lead_review_chain_handler import (
    GetLeadReviewChainHandler,
)
from app.domain.assessment.entities.assessment import Assessment
from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.entities.contact import Contact
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.contact.value_objects.email import Email
from app.domain.discovery.entities.discovery import Discovery
from app.domain.lead.entities.lead import Lead
from app.domain.recommendation.entities.recommendation import Recommendation
from app.domain.recommendation.entities.solution import Solution
from app.domain.suppression.entities.suppression_entry import SuppressionEntry


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
    return GetLeadReviewChainHandler(unit_of_work=unit_of_work)


@pytest.mark.asyncio
async def test_fresh_lead_with_no_downstream_stages_returns_all_none(handler, unit_of_work):
    lead = _lead()
    unit_of_work.lead_repository.get_by_id.return_value = lead
    unit_of_work.discovery_repository.get_by_lead.return_value = None
    unit_of_work.assessment_repository.get_by_lead_id.return_value = None
    unit_of_work.contact_repository.get_by_id.return_value = None

    result = await handler.handle(lead.id.value)

    assert result.lead.id == str(lead.id)
    assert result.discovery is None
    assert result.assessment is None
    assert result.recommendation is None
    assert result.contact_email_suppressed is False
    unit_of_work.recommendation_repository.get_by_assessment_id.assert_not_awaited()


@pytest.mark.asyncio
async def test_lead_with_discovery_but_no_assessment_yet(handler, unit_of_work):
    lead = _lead()
    discovery = Discovery(lead_id=lead.id, problem_statement="Manual monthly reporting.")
    unit_of_work.lead_repository.get_by_id.return_value = lead
    unit_of_work.discovery_repository.get_by_lead.return_value = discovery
    unit_of_work.assessment_repository.get_by_lead_id.return_value = None
    unit_of_work.contact_repository.get_by_id.return_value = None

    result = await handler.handle(lead.id.value)

    assert result.discovery is not None
    assert result.discovery.problem_statement == "Manual monthly reporting."
    assert result.assessment is None
    assert result.recommendation is None


@pytest.mark.asyncio
async def test_lead_with_the_full_chain_returns_every_stage(handler, unit_of_work):
    lead = _lead()
    discovery = Discovery(lead_id=lead.id, problem_statement="Manual monthly reporting.")
    assessment = Assessment(discovery_id=discovery.id, summary="Findings summary.")
    recommendation = Recommendation(assessment_id=assessment.id)
    recommendation.add_solution(
        Solution(
            title="Automate reporting",
            description="Automate the monthly reporting workflow.",
            solution_type="Automation",
            priority="High",
            is_existing_offering=True,
        )
    )
    unit_of_work.lead_repository.get_by_id.return_value = lead
    unit_of_work.discovery_repository.get_by_lead.return_value = discovery
    unit_of_work.assessment_repository.get_by_lead_id.return_value = assessment
    unit_of_work.recommendation_repository.get_by_assessment_id.return_value = recommendation
    unit_of_work.contact_repository.get_by_id.return_value = None

    result = await handler.handle(lead.id.value)

    assert result.discovery is not None
    assert result.assessment is not None
    assert result.recommendation is not None
    assert len(result.recommendation.solutions) == 1


@pytest.mark.asyncio
async def test_raises_not_found_for_an_unknown_lead(handler, unit_of_work):
    unit_of_work.lead_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await handler.handle(CompanyId().value)


@pytest.mark.asyncio
async def test_flags_a_suppressed_contact_email(handler, unit_of_work):
    lead = _lead()
    contact = Contact(first_name="Jane", last_name="Doe", email=Email("jane@example.com"))
    unit_of_work.lead_repository.get_by_id.return_value = lead
    unit_of_work.discovery_repository.get_by_lead.return_value = None
    unit_of_work.assessment_repository.get_by_lead_id.return_value = None
    unit_of_work.contact_repository.get_by_id.return_value = contact
    unit_of_work.suppression_repository.find_by_email.return_value = SuppressionEntry(
        email=Email("jane@example.com"),
    )

    result = await handler.handle(lead.id.value)

    assert result.contact_email_suppressed is True
    unit_of_work.suppression_repository.find_by_email.assert_awaited_once_with("jane@example.com")


@pytest.mark.asyncio
async def test_does_not_flag_a_non_suppressed_contact_email(handler, unit_of_work):
    lead = _lead()
    contact = Contact(first_name="Jane", last_name="Doe", email=Email("jane@example.com"))
    unit_of_work.lead_repository.get_by_id.return_value = lead
    unit_of_work.discovery_repository.get_by_lead.return_value = None
    unit_of_work.assessment_repository.get_by_lead_id.return_value = None
    unit_of_work.contact_repository.get_by_id.return_value = contact
    unit_of_work.suppression_repository.find_by_email.return_value = None

    result = await handler.handle(lead.id.value)

    assert result.contact_email_suppressed is False
