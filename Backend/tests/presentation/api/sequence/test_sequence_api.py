"""Tests for the Sequence endpoints (EPIC-09.1)."""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.exceptions.validation_exception import ValidationException
from app.application.sequence.dto.sequence_responses import (
    SequenceResponseDTO,
    TouchResponseDTO,
)
from app.application.sequence.handlers.advance_sequence_handler import (
    AdvanceSequenceHandler,
)
from app.application.sequence.handlers.create_sequence_handler import (
    CreateSequenceHandler,
)
from app.application.sequence.handlers.generate_sequence_content_handler import (
    GenerateSequenceContentHandler,
)
from app.application.sequence.handlers.get_sequence_handler import GetSequenceHandler
from app.application.sequence.handlers.list_sequences_handler import (
    ListSequencesHandler,
)
from app.application.sequence.handlers.record_sequence_bounce_handler import (
    RecordSequenceBounceHandler,
)
from app.application.sequence.handlers.record_sequence_reply_handler import (
    RecordSequenceReplyHandler,
)
from app.application.sequence.handlers.start_sequence_handler import (
    StartSequenceHandler,
)
from app.domain.sequence.enums.sequence_status import SequenceStatus
from app.domain.sequence.enums.touch_channel import TouchChannel
from app.presentation.api.dependencies.handlers import (
    get_advance_sequence_handler,
    get_create_sequence_handler,
    get_generate_sequence_content_handler,
    get_list_sequences_handler,
    get_record_sequence_bounce_handler,
    get_record_sequence_reply_handler,
    get_sequence_handler,
    get_start_sequence_handler,
)
from app.presentation.api.exception_handlers import register_exception_handlers
from app.presentation.api.routers.sequence_router import router

_SEQUENCE_ID = str(uuid4())
_LEAD_ID = str(uuid4())


def _dto(status: SequenceStatus = SequenceStatus.DRAFT, **overrides) -> SequenceResponseDTO:
    defaults = dict(
        id=_SEQUENCE_ID,
        lead_id=_LEAD_ID,
        touches=[TouchResponseDTO(channel=TouchChannel.EMAIL, wait_days=0)],
        status=status,
        current_touch_index=0,
    )
    defaults.update(overrides)
    return SequenceResponseDTO(**defaults)


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


def test_create_sequence_success_returns_201(app, client):
    handler = AsyncMock(spec=CreateSequenceHandler)
    handler.handle.return_value = _dto()
    app.dependency_overrides[get_create_sequence_handler] = lambda: handler

    response = client.post(
        "/sequences",
        json={"lead_id": _LEAD_ID, "touches": [{"channel": "Email", "wait_days": 0}]},
    )

    assert response.status_code == 201
    assert response.json()["lead_id"] == _LEAD_ID


def test_create_sequence_unknown_lead_returns_404(app, client):
    handler = AsyncMock(spec=CreateSequenceHandler)
    handler.handle.side_effect = NotFoundException(message="Lead not found.")
    app.dependency_overrides[get_create_sequence_handler] = lambda: handler

    response = client.post(
        "/sequences",
        json={"lead_id": _LEAD_ID, "touches": [{"channel": "Email", "wait_days": 0}]},
    )

    assert response.status_code == 404


def test_get_sequence_returns_200(app, client):
    handler = AsyncMock(spec=GetSequenceHandler)
    handler.handle.return_value = _dto()
    app.dependency_overrides[get_sequence_handler] = lambda: handler

    response = client.get(f"/sequences/{_SEQUENCE_ID}")

    assert response.status_code == 200
    assert response.json()["id"] == _SEQUENCE_ID


def test_list_sequences_requires_lead_id_and_returns_200(app, client):
    handler = AsyncMock(spec=ListSequencesHandler)
    handler.handle.return_value = [_dto()]
    app.dependency_overrides[get_list_sequences_handler] = lambda: handler

    response = client.get("/sequences", params={"lead_id": _LEAD_ID})

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_start_sequence_success_returns_200(app, client):
    handler = AsyncMock(spec=StartSequenceHandler)
    handler.handle.return_value = _dto(status=SequenceStatus.ACTIVE, started_at=datetime.now(UTC))
    app.dependency_overrides[get_start_sequence_handler] = lambda: handler

    response = client.post(f"/sequences/{_SEQUENCE_ID}/start")

    assert response.status_code == 200
    assert response.json()["status"] == "Active"


def test_start_sequence_lead_not_approved_returns_409(app, client):
    handler = AsyncMock(spec=StartSequenceHandler)
    handler.handle.side_effect = ConflictException(
        message="Lead must be approved via the review gate before starting a Sequence."
    )
    app.dependency_overrides[get_start_sequence_handler] = lambda: handler

    response = client.post(f"/sequences/{_SEQUENCE_ID}/start")

    assert response.status_code == 409


def test_advance_sequence_success_returns_200(app, client):
    handler = AsyncMock(spec=AdvanceSequenceHandler)
    handler.handle.return_value = _dto(status=SequenceStatus.ACTIVE, current_touch_index=1)
    app.dependency_overrides[get_advance_sequence_handler] = lambda: handler

    response = client.post(f"/sequences/{_SEQUENCE_ID}/advance")

    assert response.status_code == 200
    assert response.json()["current_touch_index"] == 1


def test_advance_sequence_not_active_returns_409(app, client):
    handler = AsyncMock(spec=AdvanceSequenceHandler)
    handler.handle.side_effect = ConflictException(message="Sequence must be active to advance.")
    app.dependency_overrides[get_advance_sequence_handler] = lambda: handler

    response = client.post(f"/sequences/{_SEQUENCE_ID}/advance")

    assert response.status_code == 409


def test_record_sequence_reply_success_returns_200(app, client):
    handler = AsyncMock(spec=RecordSequenceReplyHandler)
    handler.handle.return_value = _dto(status=SequenceStatus.STOPPED, stop_reason="replied")
    app.dependency_overrides[get_record_sequence_reply_handler] = lambda: handler

    response = client.post(f"/sequences/{_SEQUENCE_ID}/reply")

    assert response.status_code == 200
    assert response.json()["stop_reason"] == "replied"


def test_record_sequence_bounce_success_returns_200(app, client):
    handler = AsyncMock(spec=RecordSequenceBounceHandler)
    handler.handle.return_value = _dto(status=SequenceStatus.STOPPED, stop_reason="bounced")
    app.dependency_overrides[get_record_sequence_bounce_handler] = lambda: handler

    response = client.post(f"/sequences/{_SEQUENCE_ID}/bounce")

    assert response.status_code == 200
    assert response.json()["stop_reason"] == "bounced"


def test_generate_sequence_content_success_returns_200(app, client):
    handler = AsyncMock(spec=GenerateSequenceContentHandler)
    handler.handle.return_value = _dto(
        touches=[TouchResponseDTO(channel=TouchChannel.EMAIL, wait_days=0, content="Generated copy.")],
    )
    app.dependency_overrides[get_generate_sequence_content_handler] = lambda: handler

    response = client.post(f"/sequences/{_SEQUENCE_ID}/generate-content")

    assert response.status_code == 200
    assert response.json()["touches"][0]["content"] == "Generated copy."


def test_generate_sequence_content_not_draft_returns_409(app, client):
    handler = AsyncMock(spec=GenerateSequenceContentHandler)
    handler.handle.side_effect = ConflictException(
        message="Sequence must be in Draft status to generate content."
    )
    app.dependency_overrides[get_generate_sequence_content_handler] = lambda: handler

    response = client.post(f"/sequences/{_SEQUENCE_ID}/generate-content")

    assert response.status_code == 409


def test_generate_sequence_content_no_evidence_returns_422(app, client):
    handler = AsyncMock(spec=GenerateSequenceContentHandler)
    handler.handle.side_effect = ValidationException(message="This Lead has no captured evidence.")
    app.dependency_overrides[get_generate_sequence_content_handler] = lambda: handler

    response = client.post(f"/sequences/{_SEQUENCE_ID}/generate-content")

    assert response.status_code == 422
