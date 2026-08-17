"""
Tests for POST /auth/login and GET /auth/me
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.common.exceptions.unauthorized_exception import (
    UnauthorizedException,
)
from app.application.user.dto.login_response import LoginResponseDTO
from app.application.user.handlers.login_handler import LoginHandler
from app.domain.user.entities.user import User
from app.domain.user.value_objects.email import Email
from app.domain.user.value_objects.password_hash import PasswordHash
from app.presentation.api.dependencies.auth import get_current_user
from app.presentation.api.dependencies.handlers import get_login_handler
from app.presentation.api.exception_handlers import register_exception_handlers
from app.presentation.api.routers.auth_router import router

_VALID_HASH = "$2b$12$" + ("N" * 53)


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    register_exception_handlers(app)
    return app


@pytest.fixture
def login_handler():
    return AsyncMock(spec=LoginHandler)


@pytest.fixture
def client(app, login_handler):
    app.dependency_overrides[get_login_handler] = lambda: login_handler
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_login_success_returns_200_and_a_token(client, login_handler):
    login_handler.handle.return_value = LoginResponseDTO(
        access_token="a-real-looking-jwt",
        expires_in=28800,
        user={"id": "u1", "email": "jane@example.com", "is_active": True},
    )

    response = client.post(
        "/auth/login",
        json={"email": "jane@example.com", "password": "correct-password"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["access_token"] == "a-real-looking-jwt"
    assert body["token_type"] == "bearer"


def test_login_failure_returns_401_with_a_generic_message(client, login_handler):
    login_handler.handle.side_effect = UnauthorizedException("Invalid email or password.")

    response = client.post(
        "/auth/login",
        json={"email": "jane@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
    body = response.json()
    assert body["success"] is False
    assert body["error_code"] == "UNAUTHORIZED"
    assert body["message"] == "Invalid email or password."


def test_get_me_without_a_token_returns_401(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_get_me_with_a_valid_token_returns_the_current_user(app):
    user = User(
        email=Email("jane@example.com"),
        password_hash=PasswordHash(_VALID_HASH),
    )
    app.dependency_overrides[get_current_user] = lambda: user

    client = TestClient(app)
    response = client.get("/auth/me", headers={"Authorization": "Bearer whatever"})

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "jane@example.com"
    assert body["is_active"] is True
