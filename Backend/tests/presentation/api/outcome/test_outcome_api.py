"""Tests for the Outcome endpoints (EPIC-12)."""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.outcome.dto.outcome_responses import OutcomeEventResponseDTO
from app.application.outcome.handlers.create_outcome_event_handler import (
    CreateOutcomeEventHandler,
)
from app.application.outcome.handlers.delete_outcome_event_handler import (
    DeleteOutcomeEventHandler,
)
from app.application.outcome.handlers.list_outcome_events_handler import (
    ListOutcomeEventsHandler,
)
from app.domain.outcome.enums.outcome_type import OutcomeType
from app.presentation.api.dependencies.handlers import (
    get_create_outcome_event_handler,
    get_delete_outcome_event_handler,
    get_list_outcome_events_handler,
)
from app.presentation.api.exception_handlers import register_exception_handlers
from app.presentation.api.routers.outcome_router import router


def _event_dto() -> OutcomeEventResponseDTO:
    return OutcomeEventResponseDTO(
        id="00000000-0000-0000-0000-000000000001",
        lead_id="00000000-0000-0000-0000-000000000002",
        outcome_type=OutcomeType.MEETING_BOOKED,
        occurred_at=datetime.now(UTC),
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


def test_create_outcome_event_success_returns_201(app, client):
    handler = AsyncMock(spec=CreateOutcomeEventHandler)
    handler.handle.return_value = _event_dto()
    app.dependency_overrides[get_create_outcome_event_handler] = lambda: handler

    response = client.post(
        "/outcomes",
        json={
            "lead_id": "00000000-0000-0000-0000-000000000002",
            "outcome_type": "Meeting Booked",
        },
    )

    assert response.status_code == 201
    assert response.json()["outcome_type"] == "Meeting Booked"


def test_create_outcome_event_unknown_lead_returns_404(app, client):
    handler = AsyncMock(spec=CreateOutcomeEventHandler)
    handler.handle.side_effect = NotFoundException(message="Lead not found.")
    app.dependency_overrides[get_create_outcome_event_handler] = lambda: handler

    response = client.post(
        "/outcomes",
        json={
            "lead_id": "00000000-0000-0000-0000-000000000002",
            "outcome_type": "No Response",
        },
    )

    assert response.status_code == 404


def test_list_outcome_events_returns_200(app, client):
    handler = AsyncMock(spec=ListOutcomeEventsHandler)
    handler.handle.return_value = [_event_dto()]
    app.dependency_overrides[get_list_outcome_events_handler] = lambda: handler

    response = client.get("/outcomes")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_delete_outcome_event_success_returns_204(app, client):
    handler = AsyncMock(spec=DeleteOutcomeEventHandler)
    handler.handle.return_value = None
    app.dependency_overrides[get_delete_outcome_event_handler] = lambda: handler

    response = client.delete("/outcomes/00000000-0000-0000-0000-000000000001")

    assert response.status_code == 204


def test_delete_outcome_event_not_found_returns_404(app, client):
    handler = AsyncMock(spec=DeleteOutcomeEventHandler)
    handler.handle.side_effect = NotFoundException(message="Outcome event not found.")
    app.dependency_overrides[get_delete_outcome_event_handler] = lambda: handler

    response = client.delete("/outcomes/00000000-0000-0000-0000-000000000001")

    assert response.status_code == 404
