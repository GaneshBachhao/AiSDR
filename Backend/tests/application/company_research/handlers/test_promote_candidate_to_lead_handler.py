from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.company_research.dto.company_research_response import (
    CompanySearchResult,
    DiscoveredContact,
)
from app.application.company_research.handlers.promote_candidate_to_lead_handler import (
    PromoteCandidateToLeadHandler,
)
from app.domain.lead.enums.lead_source import LeadSource

_COMPANY_ID = str(uuid4())
_CONTACT_ID = str(uuid4())
_EXISTING_CONTACT_ID = str(uuid4())
_RESOLVED_CONTACT_ID = str(uuid4())


def _result(evidence_signals=None, **contacts_kwargs) -> CompanySearchResult:
    contacts = (
        [DiscoveredContact(name="Jane Doe", role_title="COO", **contacts_kwargs)] if contacts_kwargs else []
    )
    return CompanySearchResult(
        company_name="Acme Manufacturing",
        website="https://acme.example",
        industry="Manufacturing",
        employee_count=120,
        evidence_of_need="hiring signals",
        evidence_classification="Strong Opportunity Signal",
        business_problem_hypothesis="manual workflows",
        expected_business_impact="x",
        trigger_event="expansion",
        qualification_score=74,
        evidence_signals=evidence_signals or {},
        priority_tier="Tier B",
        recommended_outreach_angle="x",
        suggested_first_message="x",
        confidence_level="Medium",
        discovered_contacts=contacts,
    )


def _handler(uow, create_contact_handler=None, create_lead_handler=None):
    return PromoteCandidateToLeadHandler(
        unit_of_work=uow,
        create_contact_handler=create_contact_handler or AsyncMock(),
        create_lead_handler=create_lead_handler or AsyncMock(),
    )


def _uow_with(existing_contact=None, existing_leads=None):
    uow = MagicMock()
    uow.contact_repository.find_by_email = AsyncMock(return_value=existing_contact)
    uow.lead_repository.list = AsyncMock(return_value=existing_leads or [])
    return uow


@pytest.mark.asyncio
async def test_skips_when_no_discovered_contact_has_an_email():
    uow = _uow_with()
    handler = _handler(uow)

    outcome = await handler.handle(_result(), company_id=_COMPANY_ID)

    assert outcome.contact_id is None
    assert outcome.lead_id is None
    assert outcome.skipped_reason == "no_verified_email_found"


@pytest.mark.asyncio
async def test_skips_when_discovered_contacts_exist_but_none_have_email():
    result = _result()  # no contacts at all, same as none having an email
    uow = _uow_with()
    handler = _handler(uow)

    outcome = await handler.handle(result, company_id=_COMPANY_ID)

    assert outcome.skipped_reason == "no_verified_email_found"


@pytest.mark.asyncio
async def test_creates_contact_and_lead_when_a_verified_email_is_present():
    result = _result(email="jane.doe@acme.example")
    uow = _uow_with()
    create_contact_handler = AsyncMock()
    create_contact_handler.handle.return_value = MagicMock(id=_CONTACT_ID)
    create_lead_handler = AsyncMock()
    create_lead_handler.handle.return_value = MagicMock(id="lead-1")
    handler = _handler(uow, create_contact_handler, create_lead_handler)

    outcome = await handler.handle(result, company_id=_COMPANY_ID)

    assert outcome.contact_id == _CONTACT_ID
    assert outcome.lead_id == "lead-1"
    assert outcome.skipped_reason is None

    create_contact_command = create_contact_handler.handle.call_args.args[0]
    assert create_contact_command.company_id == _COMPANY_ID
    assert create_contact_command.first_name == "Jane"
    assert create_contact_command.last_name == "Doe"
    assert create_contact_command.email == "jane.doe@acme.example"
    assert create_contact_command.job_title == "COO"

    create_lead_command = create_lead_handler.handle.call_args.args[0]
    assert create_lead_command.company_id == _COMPANY_ID
    assert create_lead_command.contact_id == _CONTACT_ID
    assert create_lead_command.source == LeadSource.AI_RESEARCH.value
    assert create_lead_command.score == 74
    assert "manual workflows" in create_lead_command.notes
    assert "hiring signals" in create_lead_command.notes
    assert create_lead_command.evidence_signals is None


@pytest.mark.asyncio
async def test_threads_evidence_signals_from_the_research_result_into_the_create_lead_command():
    result = _result(
        email="jane.doe@acme.example",
        evidence_signals={"hiring": True, "growth": False},
    )
    uow = _uow_with()
    create_contact_handler = AsyncMock()
    create_contact_handler.handle.return_value = MagicMock(id=_CONTACT_ID)
    create_lead_handler = AsyncMock()
    create_lead_handler.handle.return_value = MagicMock(id="lead-1")
    handler = _handler(uow, create_contact_handler, create_lead_handler)

    await handler.handle(result, company_id=_COMPANY_ID)

    create_lead_command = create_lead_handler.handle.call_args.args[0]
    assert create_lead_command.evidence_signals == {"hiring": True, "growth": False}


@pytest.mark.asyncio
async def test_reuses_an_existing_contact_found_by_email_instead_of_creating():
    result = _result(email="jane.doe@acme.example")
    existing_contact = MagicMock()
    existing_contact.id.value = _EXISTING_CONTACT_ID
    uow = _uow_with(existing_contact=existing_contact)
    create_contact_handler = AsyncMock()
    create_lead_handler = AsyncMock()
    create_lead_handler.handle.return_value = MagicMock(id="lead-1")
    handler = _handler(uow, create_contact_handler, create_lead_handler)

    outcome = await handler.handle(result, company_id=_COMPANY_ID)

    assert outcome.contact_id == _EXISTING_CONTACT_ID
    create_contact_handler.handle.assert_not_awaited()


@pytest.mark.asyncio
async def test_conflict_on_create_resolves_to_the_now_existing_contact():
    result = _result(email="jane.doe@acme.example")
    uow = MagicMock()
    existing_after_conflict = MagicMock()
    existing_after_conflict.id.value = _RESOLVED_CONTACT_ID
    uow.contact_repository.find_by_email = AsyncMock(side_effect=[None, existing_after_conflict])
    uow.lead_repository.list = AsyncMock(return_value=[])
    create_contact_handler = AsyncMock()
    create_contact_handler.handle.side_effect = ConflictException(
        message="Contact already exists.", details={"email": "jane.doe@acme.example"}
    )
    create_lead_handler = AsyncMock()
    create_lead_handler.handle.return_value = MagicMock(id="lead-1")
    handler = _handler(uow, create_contact_handler, create_lead_handler)

    outcome = await handler.handle(result, company_id=_COMPANY_ID)

    assert outcome.contact_id == _RESOLVED_CONTACT_ID


@pytest.mark.asyncio
async def test_reuses_an_existing_lead_for_the_same_company_and_contact():
    result = _result(email="jane.doe@acme.example")
    existing_contact = MagicMock()
    existing_contact.id.value = _CONTACT_ID
    existing_lead = MagicMock()
    existing_lead.id.value = "lead-existing"
    uow = _uow_with(existing_contact=existing_contact, existing_leads=[existing_lead])
    create_lead_handler = AsyncMock()
    handler = _handler(uow, create_lead_handler=create_lead_handler)

    outcome = await handler.handle(result, company_id=_COMPANY_ID)

    assert outcome.lead_id == "lead-existing"
    create_lead_handler.handle.assert_not_awaited()


def test_split_name_handles_single_word_names():
    first, last = PromoteCandidateToLeadHandler._split_name("Cher")
    assert (first, last) == ("Cher", "Cher")


def test_split_name_handles_multi_word_last_names():
    first, last = PromoteCandidateToLeadHandler._split_name("Mary Jane Watson")
    assert (first, last) == ("Mary", "Jane Watson")
