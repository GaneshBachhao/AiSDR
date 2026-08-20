"""
Tests for the Lead review-gate endpoints (EPIC-16):
POST /leads/{id}/submit-for-review, /approve, /reject, GET /leads/{id}/review.

Regression guard: all four endpoints are new -- the handlers behind them
didn't exist before this epic. register_exception_handlers is wired in
to prove the ConflictException/NotFoundException paths produce the app's
real structured error body, not an unhandled exception.
"""

from __future__ import annotations

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.lead.dto.lead_responses import LeadResponseDTO
from app.application.lead.dto.lead_review_chain_response import LeadReviewChainResponseDTO
from app.application.lead.handlers.approve_lead_handler import ApproveLeadHandler
from app.application.lead.handlers.get_lead_review_chain_handler import (
    GetLeadReviewChainHandler,
)
from app.application.lead.handlers.reject_lead_handler import RejectLeadHandler
from app.application.lead.handlers.submit_lead_for_review_handler import (
    SubmitLeadForReviewHandler,
)
from app.domain.lead.enums.lead_review_status import LeadReviewStatus
from app.domain.lead.enums.lead_source import LeadSource
from app.domain.lead.enums.lead_status import LeadStatus
from app.presentation.api.dependencies.handlers import (
    get_approve_lead_handler,
    get_lead_review_chain_handler,
    get_reject_lead_handler,
    get_submit_lead_for_review_handler,
)
from app.presentation.api.exception_handlers import register_exception_handlers
from app.presentation.api.routers.lead_router import router

_LEAD_ID = str(uuid4())


def _dto(review_status: LeadReviewStatus) -> LeadResponseDTO:
    return LeadResponseDTO(
        id=_LEAD_ID,
        company_id=str(uuid4()),
        contact_id=str(uuid4()),
        source=LeadSource.OTHER,
        status=LeadStatus.NEW,
        score=0,
        review_status=review_status,
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


def test_submit_for_review_success_returns_200_with_pending_review(app, client):
    handler = AsyncMock(spec=SubmitLeadForReviewHandler)
    handler.handle.return_value = _dto(LeadReviewStatus.PENDING_REVIEW)
    app.dependency_overrides[get_submit_lead_for_review_handler] = lambda: handler

    response = client.post(f"/leads/{_LEAD_ID}/submit-for-review")

    assert response.status_code == 200
    assert response.json()["review_status"] == "Pending Review"


def test_submit_for_review_not_found_returns_404(app, client):
    handler = AsyncMock(spec=SubmitLeadForReviewHandler)
    handler.handle.side_effect = NotFoundException(message="Lead not found.")
    app.dependency_overrides[get_submit_lead_for_review_handler] = lambda: handler

    response = client.post(f"/leads/{_LEAD_ID}/submit-for-review")

    assert response.status_code == 404
    assert response.json()["error_code"] == "NOT_FOUND"


def test_submit_for_review_already_approved_returns_409(app, client):
    handler = AsyncMock(spec=SubmitLeadForReviewHandler)
    handler.handle.side_effect = ConflictException(message="Lead is already pending review or approved.")
    app.dependency_overrides[get_submit_lead_for_review_handler] = lambda: handler

    response = client.post(f"/leads/{_LEAD_ID}/submit-for-review")

    assert response.status_code == 409
    body = response.json()
    assert body["error_code"] == "CONFLICT"
    assert body["message"] == "Lead is already pending review or approved."


def test_approve_success_returns_200_with_approved_status(app, client):
    handler = AsyncMock(spec=ApproveLeadHandler)
    handler.handle.return_value = _dto(LeadReviewStatus.APPROVED)
    app.dependency_overrides[get_approve_lead_handler] = lambda: handler

    response = client.post(f"/leads/{_LEAD_ID}/approve")

    assert response.status_code == 200
    assert response.json()["review_status"] == "Approved"


def test_approve_accepts_an_optional_notes_body(app, client):
    handler = AsyncMock(spec=ApproveLeadHandler)
    handler.handle.return_value = _dto(LeadReviewStatus.APPROVED)
    app.dependency_overrides[get_approve_lead_handler] = lambda: handler

    response = client.post(f"/leads/{_LEAD_ID}/approve", json={"notes": "Looks solid."})

    assert response.status_code == 200
    sent_command = handler.handle.await_args.args[0]
    assert sent_command.notes == "Looks solid."


def test_approve_while_not_pending_review_returns_409(app, client):
    handler = AsyncMock(spec=ApproveLeadHandler)
    handler.handle.side_effect = ConflictException(message="Lead must be pending review before approval.")
    app.dependency_overrides[get_approve_lead_handler] = lambda: handler

    response = client.post(f"/leads/{_LEAD_ID}/approve")

    assert response.status_code == 409


def test_reject_success_returns_200_with_rejected_status(app, client):
    handler = AsyncMock(spec=RejectLeadHandler)
    handler.handle.return_value = _dto(LeadReviewStatus.REJECTED)
    app.dependency_overrides[get_reject_lead_handler] = lambda: handler

    response = client.post(f"/leads/{_LEAD_ID}/reject")

    assert response.status_code == 200
    assert response.json()["review_status"] == "Rejected"


def test_reject_while_not_pending_review_returns_409(app, client):
    handler = AsyncMock(spec=RejectLeadHandler)
    handler.handle.side_effect = ConflictException(message="Lead must be pending review before rejection.")
    app.dependency_overrides[get_reject_lead_handler] = lambda: handler

    response = client.post(f"/leads/{_LEAD_ID}/reject")

    assert response.status_code == 409


def test_review_chain_returns_lead_with_null_downstream_stages(app, client):
    handler = AsyncMock(spec=GetLeadReviewChainHandler)
    handler.handle.return_value = LeadReviewChainResponseDTO(
        lead=_dto(LeadReviewStatus.NOT_SUBMITTED),
        discovery=None,
        assessment=None,
        recommendation=None,
    )
    app.dependency_overrides[get_lead_review_chain_handler] = lambda: handler

    response = client.get(f"/leads/{_LEAD_ID}/review")

    assert response.status_code == 200
    body = response.json()
    assert body["lead"]["id"] == _LEAD_ID
    assert body["discovery"] is None
    assert body["assessment"] is None
    assert body["recommendation"] is None


def test_review_chain_not_found_returns_404(app, client):
    handler = AsyncMock(spec=GetLeadReviewChainHandler)
    handler.handle.side_effect = NotFoundException(message="Lead not found.")
    app.dependency_overrides[get_lead_review_chain_handler] = lambda: handler

    response = client.get(f"/leads/{_LEAD_ID}/review")

    assert response.status_code == 404
