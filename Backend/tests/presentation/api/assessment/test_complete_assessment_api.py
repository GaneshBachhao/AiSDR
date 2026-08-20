"""Tests for POST /assessments/{id}/complete.

Regression coverage: complete_assessment_handler.py existed as a
completely empty file with no route wired to it at all before this.
"""

from __future__ import annotations

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.assessment.dto.assessment_response import GetAssessmentResponseDTO
from app.application.assessment.handlers.complete_assessment_handler import (
    CompleteAssessmentHandler,
)
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.presentation.api.dependencies.handlers import get_complete_assessment_handler
from app.presentation.api.exception_handlers import register_exception_handlers
from app.presentation.api.routers.assessment_router import router

_ASSESSMENT_ID = str(uuid4())


def _dto(**overrides) -> GetAssessmentResponseDTO:
    defaults = dict(
        assessment_id=_ASSESSMENT_ID,
        discovery_id=str(uuid4()),
        status="Completed",
        summary=None,
        maturity_level="Initial",
        readiness_score=0,
    )
    defaults.update(overrides)
    return GetAssessmentResponseDTO(**defaults)


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


def test_complete_assessment_success_returns_200(app, client):
    handler = AsyncMock(spec=CompleteAssessmentHandler)
    handler.handle.return_value = _dto(summary="Ready for outreach.")
    app.dependency_overrides[get_complete_assessment_handler] = lambda: handler

    response = client.post(f"/assessments/{_ASSESSMENT_ID}/complete", json={"summary": "Ready for outreach."})

    assert response.status_code == 200
    assert response.json()["status"] == "Completed"
    assert response.json()["summary"] == "Ready for outreach."


def test_complete_assessment_without_a_body_returns_200(app, client):
    handler = AsyncMock(spec=CompleteAssessmentHandler)
    handler.handle.return_value = _dto()
    app.dependency_overrides[get_complete_assessment_handler] = lambda: handler

    response = client.post(f"/assessments/{_ASSESSMENT_ID}/complete")

    assert response.status_code == 200


def test_complete_assessment_unknown_returns_404(app, client):
    handler = AsyncMock(spec=CompleteAssessmentHandler)
    handler.handle.side_effect = NotFoundException(message="Assessment not found.")
    app.dependency_overrides[get_complete_assessment_handler] = lambda: handler

    response = client.post(f"/assessments/{_ASSESSMENT_ID}/complete")

    assert response.status_code == 404
