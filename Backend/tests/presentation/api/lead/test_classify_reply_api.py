"""Tests for POST /leads/{id}/classify-reply (EPIC-10.1/10.3)."""

from __future__ import annotations

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.lead.dto.reply_classification_responses import (
    ReplyClassificationResponseDTO,
)
from app.application.lead.handlers.classify_reply_handler import ClassifyReplyHandler
from app.presentation.api.dependencies.handlers import get_classify_reply_handler
from app.presentation.api.exception_handlers import register_exception_handlers
from app.presentation.api.routers.lead_router import router

_LEAD_ID = str(uuid4())


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


def test_classify_reply_success_returns_200(app, client):
    handler = AsyncMock(spec=ClassifyReplyHandler)
    handler.handle.return_value = ReplyClassificationResponseDTO(
        classification="Interested",
        confidence="HIGH",
        lead_status="Qualified",
        lead_score=70,
        sequences_stopped=["seq-1"],
    )
    app.dependency_overrides[get_classify_reply_handler] = lambda: handler

    response = client.post(f"/leads/{_LEAD_ID}/classify-reply", json={"reply_text": "Let's talk!"})

    assert response.status_code == 200
    body = response.json()
    assert body["classification"] == "Interested"
    assert body["lead_status"] == "Qualified"
    assert body["lead_score"] == 70
    assert body["sequences_stopped"] == ["seq-1"]

    sent_command = handler.handle.await_args.args[0]
    assert sent_command.lead_id == _LEAD_ID
    assert sent_command.reply_text == "Let's talk!"


def test_classify_reply_not_found_returns_404(app, client):
    handler = AsyncMock(spec=ClassifyReplyHandler)
    handler.handle.side_effect = NotFoundException(message="Lead not found.")
    app.dependency_overrides[get_classify_reply_handler] = lambda: handler

    response = client.post(f"/leads/{_LEAD_ID}/classify-reply", json={"reply_text": "hi"})

    assert response.status_code == 404
    assert response.json()["error_code"] == "NOT_FOUND"


def test_classify_reply_requires_reply_text(app, client):
    handler = AsyncMock(spec=ClassifyReplyHandler)
    app.dependency_overrides[get_classify_reply_handler] = lambda: handler

    response = client.post(f"/leads/{_LEAD_ID}/classify-reply", json={})

    assert response.status_code == 422
    handler.handle.assert_not_called()
