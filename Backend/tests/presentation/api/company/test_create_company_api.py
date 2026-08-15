"""
Tests for POST /companies
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.company.handlers.create_company_handler import (
    CreateCompanyHandler,
)
from app.presentation.api.dependencies.handlers import (
    get_create_company_handler,
)
from app.presentation.api.routers.company_router import router


@pytest.fixture
def app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def handler() -> AsyncMock:
    handler = AsyncMock(spec=CreateCompanyHandler)

    handler.handle.return_value = {
        "id": "1",
        "name": "OpenAI",
        "website": "https://openai.com",
        "industry": "AI",
        "company_size": "1000+",
        "country": "USA",
        "state": "California",
        "city": "San Francisco",
        "is_active": True,
    }

    return handler


@pytest.fixture
def client(app: FastAPI, handler: AsyncMock) -> TestClient:
    app.dependency_overrides[get_create_company_handler] = lambda: handler
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_company(client: TestClient, handler: AsyncMock):

    response = client.post(
        "/companies",
        json={
            "name": "OpenAI",
            "website": "https://openai.com",
            "industry": "AI",
            "company_size": "1000+",
            "country": "USA",
            "state": "California",
            "city": "San Francisco",
        },
    )

    assert response.status_code == 201

    handler.handle.assert_awaited_once()