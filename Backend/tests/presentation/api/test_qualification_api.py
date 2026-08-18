"""
Tests for the Qualification API router.

Regression guard: unlike every other CRUD router, none of these endpoints
used to declare response_model=, so the generated OpenAPI schema typed
every response body as `unknown` -- the frontend had to hand-write
QualificationResponseDTO instead of generating it. These tests exist to
prove the now-declared response_model= actually matches what the real
handlers return (FastAPI validates outgoing responses against
response_model=, so a mismatch here would itself become a test failure).
"""

from __future__ import annotations

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.qualification.dto.qualification_response import (
    CreateQualificationResponseDTO,
    GetQualificationResponseDTO,
    ListQualificationResponseDTO,
    UpdateQualificationResponseDTO,
)
from app.application.qualification.handlers.create_qualification_handler import (
    CreateQualificationHandler,
)
from app.application.qualification.handlers.get_qualification_handler import (
    GetQualificationHandler,
)
from app.application.qualification.handlers.list_qualification_handler import (
    ListQualificationHandler,
)
from app.application.qualification.handlers.update_qualification_handler import (
    UpdateQualificationHandler,
)
from app.presentation.api.dependencies.handlers import (
    get_create_qualification_handler,
    get_get_qualification_handler,
    get_list_qualification_handler,
    get_update_qualification_handler,
)
from app.presentation.api.routers.qualification_router import router

_LEAD_ID = uuid4()
_ASSESSMENT_ID = uuid4()
_QUALIFICATION_ID = uuid4()


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app):
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_qualification_response_matches_the_declared_response_model(app, client):
    handler = AsyncMock(spec=CreateQualificationHandler)
    handler.handle.return_value = CreateQualificationResponseDTO(
        qualification_id=_QUALIFICATION_ID,
        lead_id=_LEAD_ID,
        assessment_id=_ASSESSMENT_ID,
        status="Partially Qualified",
        score=0,
        recommendation=None,
    )
    app.dependency_overrides[get_create_qualification_handler] = lambda: handler

    response = client.post(
        "/qualifications",
        json={"lead_id": str(_LEAD_ID), "assessment_id": str(_ASSESSMENT_ID)},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["qualification_id"] == str(_QUALIFICATION_ID)
    assert body["status"] == "Partially Qualified"


def test_get_qualification_response_matches_the_declared_response_model(app, client):
    handler = AsyncMock(spec=GetQualificationHandler)
    handler.handle.return_value = GetQualificationResponseDTO(
        qualification_id=_QUALIFICATION_ID,
        lead_id=_LEAD_ID,
        assessment_id=_ASSESSMENT_ID,
        status="Qualified",
        score=88,
        recommendation="Proceed to outreach.",
    )
    app.dependency_overrides[get_get_qualification_handler] = lambda: handler

    response = client.get(f"/qualifications/{_QUALIFICATION_ID}")

    assert response.status_code == 200
    body = response.json()
    assert body["score"] == 88
    assert body["recommendation"] == "Proceed to outreach."


def test_list_qualifications_response_matches_the_declared_response_model_and_omits_recommendation(
    app, client
):
    handler = AsyncMock(spec=ListQualificationHandler)
    handler.handle.return_value = [
        ListQualificationResponseDTO(
            qualification_id=_QUALIFICATION_ID,
            lead_id=_LEAD_ID,
            assessment_id=_ASSESSMENT_ID,
            status="Qualified",
            score=88,
        )
    ]
    app.dependency_overrides[get_list_qualification_handler] = lambda: handler

    response = client.get("/qualifications")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert "recommendation" not in body[0]


def test_update_qualification_response_matches_the_declared_response_model(app, client):
    handler = AsyncMock(spec=UpdateQualificationHandler)
    handler.handle.return_value = UpdateQualificationResponseDTO(
        qualification_id=_QUALIFICATION_ID,
        lead_id=_LEAD_ID,
        assessment_id=_ASSESSMENT_ID,
        status="Qualified",
        score=90,
        recommendation="Strong fit.",
    )
    app.dependency_overrides[get_update_qualification_handler] = lambda: handler

    response = client.put(
        f"/qualifications/{_QUALIFICATION_ID}",
        json={"status": "Qualified", "score": 90, "recommendation": "Strong fit."},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["score"] == 90
