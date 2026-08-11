"""
Tests for GET /companies
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.company.handlers.list_company_handler import (
    ListCompanyHandler,
)
from app.presentation.api.dependencies.handlers import (
    get_list_company_handler,
)
from app.presentation.api.routers.company_router import router


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def handler():

    handler = AsyncMock(spec=ListCompanyHandler)

    handler.handle.return_value = []

    return handler


@pytest.fixture
def client(app, handler):

    app.dependency_overrides[
        get_list_company_handler
    ] = lambda: handler

    yield TestClient(app)

    app.dependency_overrides.clear()


def test_list_companies(client, handler):

    response = client.get("/companies")

    assert response.status_code == 200

    handler.handle.assert_awaited_once()