"""
Integration-level regression test for Track 1 Phase 3 story 3.4:
running the same research result through promotion twice must not
duplicate the Company row -- exercised against a real in-memory DB, a
real SqlAlchemyUnitOfWork, and the real CreateCompanyHandler (not mocks).
"""

from __future__ import annotations

import pytest
from sqlalchemy import func, select

from app.application.company.company_mapper import CompanyMapper
from app.application.company.company_validator import CompanyValidator
from app.application.company.handlers.create_company_handler import CreateCompanyHandler
from app.application.company_research.dto.company_research_response import (
    CompanySearchResult,
)
from app.application.company_research.handlers.promote_candidate_to_company_handler import (
    PromoteCandidateToCompanyHandler,
)
from app.infrastructure.persistence.models.company_model import CompanyModel
from app.infrastructure.persistence.unit_of_work.sqlalchemy_unit_of_work import (
    SqlAlchemyUnitOfWork,
)


def _result() -> CompanySearchResult:
    return CompanySearchResult(
        company_name="Acme Manufacturing",
        website="https://acme.example",
        industry="Manufacturing",
        employee_count=120,
        evidence_of_need="x",
        evidence_classification="Strong Opportunity Signal",
        business_problem_hypothesis="x",
        expected_business_impact="x",
        qualification_score=60,
        priority_tier="Tier B",
        recommended_outreach_angle="x",
        suggested_first_message="x",
        confidence_level="Medium",
    )


async def _company_row_count(session) -> int:
    result = await session.execute(select(func.count()).select_from(CompanyModel))
    return result.scalar_one()


@pytest.mark.asyncio
async def test_promoting_the_same_result_twice_creates_only_one_company(async_session):
    uow = SqlAlchemyUnitOfWork(session=async_session)
    create_handler = CreateCompanyHandler(
        unit_of_work=uow,
        validator=CompanyValidator(),
        mapper=CompanyMapper(),
    )
    promoter = PromoteCandidateToCompanyHandler(uow, create_handler)

    first_id = await promoter.handle(_result())
    second_id = await promoter.handle(_result())

    assert first_id == second_id
    assert await _company_row_count(async_session) == 1


@pytest.mark.asyncio
async def test_promoting_a_name_variant_with_the_same_website_still_dedups(async_session):
    """Even if a later research run produces a slightly different company
    name for the same real company, matching by website (not just exact
    name) must still resolve to the same Company row."""
    uow = SqlAlchemyUnitOfWork(session=async_session)
    create_handler = CreateCompanyHandler(
        unit_of_work=uow,
        validator=CompanyValidator(),
        mapper=CompanyMapper(),
    )
    promoter = PromoteCandidateToCompanyHandler(uow, create_handler)

    first_id = await promoter.handle(_result())

    variant = _result().model_copy(update={"company_name": "Acme Manufacturing Pvt Ltd"})
    second_id = await promoter.handle(variant)

    assert first_id == second_id
    assert await _company_row_count(async_session) == 1
