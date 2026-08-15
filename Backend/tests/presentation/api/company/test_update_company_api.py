"""
Tests for PUT /companies/{company_id}
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.company.handlers.update_company_handler import (
    UpdateCompanyHandler,
)
from app.presentation.api.dependencies.handlers import (
    get_update_company_handler,
)
from app.presentation.api.routers.company_router import router


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def handler():

    handler = AsyncMock(spec=UpdateCompanyHandler)

    handler.handle.return_value = {
        "id": "1",
        "name": "Updated Company",
    }

    return handler


@pytest.fixture
def client(app, handler):

    app.dependency_overrides[
        get_update_company_handler
    ] = lambda: handler

    yield TestClient(app)

    app.dependency_overrides.clear()


def test_update_company(client, handler):

    response = client.put(
        "/companies/1",
        json={
            "name": "Updated Company",
        },
    )

    assert response.status_code == 200

    handler.handle.assert_awaited_once()