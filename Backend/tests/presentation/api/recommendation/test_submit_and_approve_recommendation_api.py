"""
Tests for POST /recommendations/{id}/submit, /approve, and /reject.

Regression guard: all three endpoints are new -- the handlers behind them
existed as real code (or, for reject, didn't exist at all until now) but
were never reachable from any router before this. register_exception_handlers
is wired in here (unlike some of the older isolated-router tests)
specifically to prove the new ConflictException path (submit with no
solutions / approve while still Draft) produces the app's real structured
error body, not an unhandled exception.
"""

from __future__ import annotations

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.recommendation.dto.recommendation_dto import RecommendationDTO
from app.application.recommendation.handlers.approve_recommendation_handler import (
    ApproveRecommendationHandler,
)
from app.application.recommendation.handlers.reject_recommendation_handler import (
    RejectRecommendationHandler,
)
from app.application.recommendation.handlers.submit_recommendation_handler import (
    SubmitRecommendationHandler,
)
from app.presentation.api.dependencies.handlers import (
    get_approve_recommendation_handler,
    get_reject_recommendation_handler,
    get_submit_recommendation_handler,
)
from app.presentation.api.exception_handlers import register_exception_handlers
from app.presentation.api.routers.recommendation_router import router

_RECOMMENDATION_ID = uuid4()
_ASSESSMENT_ID = uuid4()


def _dto(status: str) -> RecommendationDTO:
    return RecommendationDTO(
        id=_RECOMMENDATION_ID,
        assessment_id=_ASSESSMENT_ID,
        status=status,
        executive_summary=None,
        submitted_at=None,
        approved_at=None,
        solutions=[],
        roadmap_phases=[],
        created_at=None,
        updated_at=None,
    )


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    register_exception_handlers(app)
    return app


@pytest.fixture
def client(app):
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_submit_success_returns_200_with_under_review_status(app, client):
    handler = AsyncMock(spec=SubmitRecommendationHandler)
    handler.handle.return_value = _dto("Under Review")
    app.dependency_overrides[get_submit_recommendation_handler] = lambda: handler

    response = client.post(f"/recommendations/{_RECOMMENDATION_ID}/submit")

    assert response.status_code == 200
    assert response.json()["status"] == "Under Review"


def test_submit_not_found_returns_404(app, client):
    handler = AsyncMock(spec=SubmitRecommendationHandler)
    handler.handle.side_effect = NotFoundException(message="Recommendation not found.")
    app.dependency_overrides[get_submit_recommendation_handler] = lambda: handler

    response = client.post(f"/recommendations/{_RECOMMENDATION_ID}/submit")

    assert response.status_code == 404
    assert response.json()["error_code"] == "NOT_FOUND"


def test_submit_with_no_solutions_returns_409(app, client):
    handler = AsyncMock(spec=SubmitRecommendationHandler)
    handler.handle.side_effect = ConflictException(
        message="Recommendation must contain at least one solution."
    )
    app.dependency_overrides[get_submit_recommendation_handler] = lambda: handler

    response = client.post(f"/recommendations/{_RECOMMENDATION_ID}/submit")

    assert response.status_code == 409
    body = response.json()
    assert body["error_code"] == "CONFLICT"
    assert body["message"] == "Recommendation must contain at least one solution."


def test_approve_success_returns_200_with_approved_status(app, client):
    handler = AsyncMock(spec=ApproveRecommendationHandler)
    handler.handle.return_value = _dto("Approved")
    app.dependency_overrides[get_approve_recommendation_handler] = lambda: handler

    response = client.post(f"/recommendations/{_RECOMMENDATION_ID}/approve")

    assert response.status_code == 200
    assert response.json()["status"] == "Approved"


def test_approve_while_still_draft_returns_409(app, client):
    handler = AsyncMock(spec=ApproveRecommendationHandler)
    handler.handle.side_effect = ConflictException(
        message="Recommendation must be under review before approval."
    )
    app.dependency_overrides[get_approve_recommendation_handler] = lambda: handler

    response = client.post(f"/recommendations/{_RECOMMENDATION_ID}/approve")

    assert response.status_code == 409


def test_reject_success_returns_200_with_rejected_status(app, client):
    handler = AsyncMock(spec=RejectRecommendationHandler)
    handler.handle.return_value = _dto("Rejected")
    app.dependency_overrides[get_reject_recommendation_handler] = lambda: handler

    response = client.post(f"/recommendations/{_RECOMMENDATION_ID}/reject")

    assert response.status_code == 200
    assert response.json()["status"] == "Rejected"


def test_reject_not_found_returns_404(app, client):
    handler = AsyncMock(spec=RejectRecommendationHandler)
    handler.handle.side_effect = NotFoundException(message="Recommendation not found.")
    app.dependency_overrides[get_reject_recommendation_handler] = lambda: handler

    response = client.post(f"/recommendations/{_RECOMMENDATION_ID}/reject")

    assert response.status_code == 404
