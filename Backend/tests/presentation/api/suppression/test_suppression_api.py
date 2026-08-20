"""Tests for the Suppression endpoints (EPIC-11)."""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.suppression.dto.suppression_responses import (
    SuppressionCheckResponseDTO,
    SuppressionEntryResponseDTO,
)
from app.application.suppression.handlers.check_suppression_handler import (
    CheckSuppressionHandler,
)
from app.application.suppression.handlers.create_suppression_handler import (
    CreateSuppressionHandler,
)
from app.application.suppression.handlers.delete_suppression_handler import (
    DeleteSuppressionHandler,
)
from app.application.suppression.handlers.list_suppressions_handler import (
    ListSuppressionsHandler,
)
from app.domain.suppression.enums.suppression_reason import SuppressionReason
from app.presentation.api.dependencies.handlers import (
    get_check_suppression_handler,
    get_create_suppression_handler,
    get_delete_suppression_handler,
    get_list_suppressions_handler,
)
from app.presentation.api.exception_handlers import register_exception_handlers
from app.presentation.api.routers.suppression_router import router


def _entry_dto() -> SuppressionEntryResponseDTO:
    return SuppressionEntryResponseDTO(
        id="00000000-0000-0000-0000-000000000001",
        email="foo@bar.com",
        reason=SuppressionReason.MANUAL,
        suppressed_at=datetime.now(UTC),
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


def test_create_suppression_success_returns_200(app, client):
    handler = AsyncMock(spec=CreateSuppressionHandler)
    handler.handle.return_value = _entry_dto()
    app.dependency_overrides[get_create_suppression_handler] = lambda: handler

    response = client.post("/suppressions", json={"email": "foo@bar.com"})

    assert response.status_code == 200
    assert response.json()["email"] == "foo@bar.com"


def test_list_suppressions_returns_200(app, client):
    handler = AsyncMock(spec=ListSuppressionsHandler)
    handler.handle.return_value = [_entry_dto()]
    app.dependency_overrides[get_list_suppressions_handler] = lambda: handler

    response = client.get("/suppressions")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_check_suppression_returns_the_check_result(app, client):
    handler = AsyncMock(spec=CheckSuppressionHandler)
    handler.handle.return_value = SuppressionCheckResponseDTO(
        email="foo@bar.com", suppressed=True, entry=_entry_dto()
    )
    app.dependency_overrides[get_check_suppression_handler] = lambda: handler

    response = client.get("/suppressions/check", params={"email": "foo@bar.com"})

    assert response.status_code == 200
    body = response.json()
    assert body["suppressed"] is True
    assert body["entry"]["email"] == "foo@bar.com"


def test_delete_suppression_success_returns_204(app, client):
    handler = AsyncMock(spec=DeleteSuppressionHandler)
    handler.handle.return_value = None
    app.dependency_overrides[get_delete_suppression_handler] = lambda: handler

    response = client.delete("/suppressions/00000000-0000-0000-0000-000000000001")

    assert response.status_code == 204


def test_delete_suppression_not_found_returns_404(app, client):
    handler = AsyncMock(spec=DeleteSuppressionHandler)
    handler.handle.side_effect = NotFoundException(message="Suppression entry not found.")
    app.dependency_overrides[get_delete_suppression_handler] = lambda: handler

    response = client.delete("/suppressions/00000000-0000-0000-0000-000000000001")

    assert response.status_code == 404
