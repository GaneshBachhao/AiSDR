from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.company.dto.company_responses import CompanyResponseDTO
from app.application.company_research.dto.company_research_response import (
    CompanySearchResult,
)
from app.application.company_research.handlers.promote_candidate_to_company_handler import (
    PromoteCandidateToCompanyHandler,
)


def _result(name: str = "Acme Manufacturing", website: str | None = "https://acme.example") -> CompanySearchResult:
    return CompanySearchResult(
        company_name=name,
        website=website,
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


class _FakeCompany:
    def __init__(self, id_value: str) -> None:
        class _Id:
            def __init__(self, value: str) -> None:
                self.value = value

        self.id = _Id(id_value)


def _fake_uow(find_by_website=None, find_by_name=None):
    uow = AsyncMock()
    repo = AsyncMock()
    repo.find_by_website.return_value = find_by_website
    repo.find_by_name.return_value = find_by_name
    uow.company_repository = repo
    return uow


@pytest.mark.asyncio
async def test_matches_by_website_without_calling_create_handler():
    uow = _fake_uow(find_by_website=_FakeCompany("existing-id"))
    create_handler = AsyncMock()
    handler = PromoteCandidateToCompanyHandler(uow, create_handler)

    company_id = await handler.handle(_result())

    assert company_id == "existing-id"
    create_handler.handle.assert_not_awaited()


@pytest.mark.asyncio
async def test_creates_a_new_company_when_no_match_found():
    uow = _fake_uow(find_by_website=None)
    create_handler = AsyncMock()
    create_handler.handle.return_value = CompanyResponseDTO(id="new-id", name="Acme Manufacturing")
    handler = PromoteCandidateToCompanyHandler(uow, create_handler)

    company_id = await handler.handle(_result())

    assert company_id == "new-id"
    create_handler.handle.assert_awaited_once()


@pytest.mark.asyncio
async def test_falls_back_to_name_match_on_conflict():
    uow = _fake_uow(find_by_website=None, find_by_name=_FakeCompany("existing-by-name"))
    create_handler = AsyncMock()
    create_handler.handle.side_effect = ConflictException(message="Company already exists.")
    handler = PromoteCandidateToCompanyHandler(uow, create_handler)

    company_id = await handler.handle(_result())

    assert company_id == "existing-by-name"


@pytest.mark.asyncio
async def test_reraises_conflict_when_name_lookup_also_finds_nothing():
    uow = _fake_uow(find_by_website=None, find_by_name=None)
    create_handler = AsyncMock()
    create_handler.handle.side_effect = ConflictException(message="Company already exists.")
    handler = PromoteCandidateToCompanyHandler(uow, create_handler)

    with pytest.raises(ConflictException):
        await handler.handle(_result())


@pytest.mark.asyncio
async def test_no_website_skips_website_lookup_entirely():
    uow = _fake_uow(find_by_website=None)
    create_handler = AsyncMock()
    create_handler.handle.return_value = CompanyResponseDTO(id="new-id", name="Acme Manufacturing")
    handler = PromoteCandidateToCompanyHandler(uow, create_handler)

    await handler.handle(_result(website=None))

    uow.company_repository.find_by_website.assert_not_awaited()
