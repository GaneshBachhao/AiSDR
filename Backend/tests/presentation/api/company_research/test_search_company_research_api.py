"""
Tests for POST /company-research/search
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.company_research.dto.company_research_response import (
    CandidateResearchFailure,
    CompanyResearchBatchResult,
    CompanySearchResult,
)
from app.application.company_research.handlers.search_companies_handler import (
    SearchCompaniesHandler,
)
from app.infrastructure.ai.exceptions.ai_budget_exceeded_exception import (
    AIBudgetExceededException,
)
from app.presentation.api.dependencies.company_research import (
    get_search_companies_handler,
)
from app.presentation.api.routers.company_research_router import router


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def handler():
    handler = AsyncMock(spec=SearchCompaniesHandler)
    handler.handle.return_value = CompanyResearchBatchResult(
        results=[
            CompanySearchResult(
                company_name="Example Manufacturing",
                industry="Manufacturing",
                location="India",
                website="https://example.com",
                evidence_of_need="Public sources show a technology hiring signal.",
                evidence_classification="Strong Opportunity Signal",
                business_problem_hypothesis="The company may benefit from reviewing workflow and technology integration.",
                recommended_solution=["Custom Application Development"],
                expected_business_impact="Potentially less manual work and easier scaling.",
                opportunity_type=["Cloud / Software Modernization"],
                qualification_score=62,
                priority_tier="Tier B",
                recommended_outreach_angle="A focused technology review may be useful.",
                suggested_first_message="Subject: Technology improvement opportunity\n\nHello.",
                confidence_level="Medium",
                sources=[],
            )
        ]
    )
    return handler


@pytest.fixture
def client(app, handler):
    app.dependency_overrides[get_search_companies_handler] = lambda: handler
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_route_is_registered_in_openapi(app):
    paths = app.openapi()["paths"]
    assert "/company-research/search" in paths
    assert "post" in paths["/company-research/search"]


def test_search_companies_returns_handler_results(client, handler):
    payload = {
        "industries": ["Manufacturing"],
        "geography": "India",
        "number_of_companies": 1,
        "minimum_qualification_score": 60,
    }

    response = client.post("/company-research/search", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert len(body["results"]) == 1
    assert body["results"][0]["company_name"] == "Example Manufacturing"
    assert body["results"][0]["qualification_score"] == 62
    assert body["failures"] == []
    handler.handle.assert_awaited_once()


def test_search_companies_maps_handler_exception_to_502(client, handler):
    handler.handle.side_effect = RuntimeError("upstream search failed")

    response = client.post("/company-research/search", json={"geography": "India"})

    assert response.status_code == 502
    assert "Company research failed" in response.json()["detail"]


def test_search_companies_maps_budget_exceeded_to_429(client, handler):
    handler.handle.side_effect = AIBudgetExceededException(
        "Requested 10 AI calls against 'gemini' but only 3 remain in today's budget."
    )

    response = client.post("/company-research/search", json={"geography": "India"})

    assert response.status_code == 429
    assert "only 3 remain" in response.json()["detail"]


def test_route_retry_is_registered_in_openapi(app):
    paths = app.openapi()["paths"]
    assert "/company-research/retry" in paths
    assert "post" in paths["/company-research/retry"]


def _retry_payload() -> dict:
    return {
        "failure": {
            "company_name": "Acme Manufacturing",
            "website": "https://acme.example",
            "title": "Acme Manufacturing",
            "content": "x",
            "source_url": "https://acme.example",
            "failed_step": "identity_verification",
            "error_message": "tavily unreachable",
        },
        "request": {"geography": "India"},
    }


def test_retry_candidate_returns_a_qualified_result(client, handler):
    handler.retry_candidate.return_value = CompanySearchResult(
        company_name="Acme Manufacturing",
        evidence_of_need="x",
        evidence_classification="Strong Opportunity Signal",
        business_problem_hypothesis="x",
        expected_business_impact="x",
        qualification_score=70,
        priority_tier="Tier B",
        recommended_outreach_angle="x",
        suggested_first_message="x",
        confidence_level="Medium",
    )

    response = client.post("/company-research/retry", json=_retry_payload())

    assert response.status_code == 200
    assert response.json()["company_name"] == "Acme Manufacturing"
    handler.retry_candidate.assert_awaited_once()


def test_retry_candidate_returns_another_failure(client, handler):
    handler.retry_candidate.return_value = CandidateResearchFailure(
        company_name="Acme Manufacturing",
        title="Acme Manufacturing",
        content="x",
        source_url="https://acme.example",
        failed_step="identity_verification",
        error_message="tavily unreachable again",
    )

    response = client.post("/company-research/retry", json=_retry_payload())

    assert response.status_code == 200
    assert response.json()["failed_step"] == "identity_verification"


def test_retry_candidate_returns_null_when_no_longer_qualifying(client, handler):
    handler.retry_candidate.return_value = None

    response = client.post("/company-research/retry", json=_retry_payload())

    assert response.status_code == 200
    assert response.json() is None


def test_retry_candidate_maps_budget_exceeded_to_429(client, handler):
    handler.retry_candidate.side_effect = AIBudgetExceededException(
        "Requested 1 AI call against 'gemini' but only 0 remain in today's budget."
    )

    response = client.post("/company-research/retry", json=_retry_payload())

    assert response.status_code == 429
