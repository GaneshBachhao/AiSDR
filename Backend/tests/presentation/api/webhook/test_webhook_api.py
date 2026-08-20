"""Tests for POST /webhooks/email-events (EPIC-11)."""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.suppression.dto.suppression_responses import (
    SuppressionEntryResponseDTO,
)
from app.application.suppression.handlers.record_email_event_handler import (
    RecordEmailEventHandler,
)
from app.domain.suppression.enums.suppression_reason import SuppressionReason
from app.infrastructure.configuration.webhook_settings import WebhookSettings
from app.presentation.api.dependencies.handlers import get_record_email_event_handler
from app.presentation.api.dependencies.webhooks import get_webhook_settings
from app.presentation.api.exception_handlers import register_exception_handlers
from app.presentation.api.routers.webhook_router import router


def _entry_dto() -> SuppressionEntryResponseDTO:
    return SuppressionEntryResponseDTO(
        id="00000000-0000-0000-0000-000000000001",
        email="bounced@example.com",
        reason=SuppressionReason.BOUNCE,
        suppressed_at=datetime.now(UTC),
    )


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    register_exception_handlers(app)
    app.dependency_overrides[get_webhook_settings] = lambda: WebhookSettings(
        email_webhook_secret="test-secret"
    )
    return app


@pytest.fixture
def client(app):
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_valid_secret_reaches_the_handler(app, client):
    handler = AsyncMock(spec=RecordEmailEventHandler)
    handler.handle.return_value = _entry_dto()
    app.dependency_overrides[get_record_email_event_handler] = lambda: handler

    response = client.post(
        "/webhooks/email-events",
        json={"email": "bounced@example.com", "event_type": "bounce"},
        headers={"X-Webhook-Secret": "test-secret"},
    )

    assert response.status_code == 200
    assert response.json()["reason"] == "Bounce"


def test_wrong_secret_returns_401(app, client):
    handler = AsyncMock(spec=RecordEmailEventHandler)
    app.dependency_overrides[get_record_email_event_handler] = lambda: handler

    response = client.post(
        "/webhooks/email-events",
        json={"email": "bounced@example.com", "event_type": "bounce"},
        headers={"X-Webhook-Secret": "wrong-secret"},
    )

    assert response.status_code == 401
    handler.handle.assert_not_awaited()


def test_missing_secret_header_returns_401(app, client):
    handler = AsyncMock(spec=RecordEmailEventHandler)
    app.dependency_overrides[get_record_email_event_handler] = lambda: handler

    response = client.post(
        "/webhooks/email-events",
        json={"email": "bounced@example.com", "event_type": "bounce"},
    )

    assert response.status_code == 401
    handler.handle.assert_not_awaited()
