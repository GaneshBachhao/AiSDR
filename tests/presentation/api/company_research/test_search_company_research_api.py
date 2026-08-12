"""
Tests for POST /company-research/search
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.company_research.dto.company_research_response import (
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
    handler.handle.return_value = [
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
    assert len(body) == 1
    assert body[0]["company_name"] == "Example Manufacturing"
    assert body[0]["qualification_score"] == 62
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
