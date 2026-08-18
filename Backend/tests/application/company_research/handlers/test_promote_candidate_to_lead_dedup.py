"""
Integration-level regression test for Track 1 Phase 6 story 6.3:
running the same qualified, already-Company-promoted research result
through Lead promotion twice must produce exactly one Contact and one
Lead -- exercised against a real in-memory DB, a real
``SqlAlchemyUnitOfWork``, and the real Create{Contact,Lead}Handlers (not
mocks). Uses a scripted ``email`` on the discovered contact since no real
email source exists in the live pipeline yet (see
``promote_candidate_to_lead_handler.py`` module docstring) -- this proves
the bridge mechanism itself is correct, independent of that gap.
"""

from __future__ import annotations

import pytest
from sqlalchemy import func, select

from app.application.company.company_mapper import CompanyMapper
from app.application.company.company_validator import CompanyValidator
from app.application.company.handlers.create_company_handler import CreateCompanyHandler
from app.application.company_research.dto.company_research_response import (
    CompanySearchResult,
    DiscoveredContact,
)
from app.application.company_research.handlers.promote_candidate_to_company_handler import (
    PromoteCandidateToCompanyHandler,
)
from app.application.company_research.handlers.promote_candidate_to_lead_handler import (
    PromoteCandidateToLeadHandler,
)
from app.application.contact.contact_mapper import ContactMapper
from app.application.contact.contact_validator import ContactValidator
from app.application.contact.handlers.create_contact_handler import CreateContactHandler
from app.application.lead.handlers.create_lead_handler import CreateLeadHandler
from app.domain.lead.enums.lead_source import LeadSource
from app.infrastructure.persistence.models.contact_model import ContactModel
from app.infrastructure.persistence.models.lead_model import LeadModel
from app.infrastructure.persistence.unit_of_work.sqlalchemy_unit_of_work import (
    SqlAlchemyUnitOfWork,
)


def _result() -> CompanySearchResult:
    return CompanySearchResult(
        company_name="Acme Manufacturing",
        website="https://acme.example",
        industry="Manufacturing",
        employee_count=120,
        evidence_of_need="hiring signals",
        evidence_classification="Strong Opportunity Signal",
        business_problem_hypothesis="manual workflows",
        expected_business_impact="x",
        qualification_score=74,
        priority_tier="Tier B",
        recommended_outreach_angle="x",
        suggested_first_message="x",
        confidence_level="Medium",
        discovered_contacts=[
            DiscoveredContact(name="Jane Doe", role_title="COO", email="jane.doe@acme.example")
        ],
    )


async def _row_count(session, model) -> int:
    result = await session.execute(select(func.count()).select_from(model))
    return result.scalar_one()


@pytest.mark.asyncio
async def test_promoting_the_same_result_twice_creates_only_one_contact_and_one_lead(
    async_session,
):
    uow = SqlAlchemyUnitOfWork(session=async_session)
    company_promoter = PromoteCandidateToCompanyHandler(
        uow,
        CreateCompanyHandler(unit_of_work=uow, validator=CompanyValidator(), mapper=CompanyMapper()),
    )
    lead_promoter = PromoteCandidateToLeadHandler(
        unit_of_work=uow,
        create_contact_handler=CreateContactHandler(
            unit_of_work=uow, validator=ContactValidator(), mapper=ContactMapper()
        ),
        create_lead_handler=CreateLeadHandler(unit_of_work=uow),
    )

    result = _result()
    company_id = await company_promoter.handle(result)
    first_outcome = await lead_promoter.handle(result, company_id)
    second_outcome = await lead_promoter.handle(result, company_id)

    assert first_outcome.contact_id == second_outcome.contact_id
    assert first_outcome.lead_id == second_outcome.lead_id
    assert first_outcome.skipped_reason is None
    assert await _row_count(async_session, ContactModel) == 1
    assert await _row_count(async_session, LeadModel) == 1


@pytest.mark.asyncio
async def test_promoted_lead_carries_ai_research_source_and_score_hypothesis_evidence(
    async_session,
):
    uow = SqlAlchemyUnitOfWork(session=async_session)
    company_promoter = PromoteCandidateToCompanyHandler(
        uow,
        CreateCompanyHandler(unit_of_work=uow, validator=CompanyValidator(), mapper=CompanyMapper()),
    )
    lead_promoter = PromoteCandidateToLeadHandler(
        unit_of_work=uow,
        create_contact_handler=CreateContactHandler(
            unit_of_work=uow, validator=ContactValidator(), mapper=ContactMapper()
        ),
        create_lead_handler=CreateLeadHandler(unit_of_work=uow),
    )

    result = _result()
    company_id = await company_promoter.handle(result)
    outcome = await lead_promoter.handle(result, company_id)

    from app.domain.lead.identifiers.lead_id import LeadId

    lead = await uow.lead_repository.get_by_id(LeadId(outcome.lead_id))
    assert lead is not None
    assert lead.source == LeadSource.AI_RESEARCH
    assert lead.score.value == 74
    assert "manual workflows" in lead.notes
    assert "hiring signals" in lead.notes
