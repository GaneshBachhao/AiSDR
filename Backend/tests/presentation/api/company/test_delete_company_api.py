"""
Tests for DELETE /companies/{company_id}
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.company.handlers.delete_company_handler import (
    DeleteCompanyHandler,
)
from app.presentation.api.dependencies.handlers import (
    get_delete_company_handler,
)
from app.presentation.api.routers.company_router import router


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def handler():

    return AsyncMock(
        spec=DeleteCompanyHandler,
    )


@pytest.fixture
def client(app, handler):

    app.dependency_overrides[get_delete_company_handler] = lambda: handler

    yield TestClient(app)

    app.dependency_overrides.clear()


def test_delete_company(client, handler):

    response = client.delete(
        "/companies/1",
    )

    assert response.status_code == 204

    handler.handle.assert_awaited_once()
