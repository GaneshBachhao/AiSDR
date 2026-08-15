"""
Tests for GET /companies/search
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.company.handlers.search_company_handler import (
    SearchCompanyHandler,
)
from app.presentation.api.dependencies.handlers import (
    get_search_company_handler,
)
from app.presentation.api.routers.company_router import router


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def handler():

    handler = AsyncMock(spec=SearchCompanyHandler)

    handler.handle.return_value = []

    return handler


@pytest.fixture
def client(app, handler):

    app.dependency_overrides[
        get_search_company_handler
    ] = lambda: handler

    yield TestClient(app)

    app.dependency_overrides.clear()


def test_search_companies(client, handler):

    response = client.get(
        "/companies/search?query=openai"
    )

    assert response.status_code == 200

    handler.handle.assert_awaited_once()