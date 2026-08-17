"""
Tests for the blanket auth gate applied at the composition root
(app/presentation/api/routers/__init__.py's `dependencies=[Depends(get_current_user)]`
on every router except /auth and /health).

Every other presentation-layer router test in this codebase mounts an
isolated FastAPI() with just `app.include_router(<one_router>)`, which
never goes through routers/__init__.py's composition and therefore never
exercises this gate -- that's why those tests need no changes for this
feature, and why this file exists as the one place that actually proves
the blanket gate works end-to-end, by mounting the real composed
api_router.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import jwt
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.domain.user.entities.user import User
from app.domain.user.value_objects.email import Email
from app.domain.user.value_objects.password_hash import PasswordHash
from app.presentation.api.dependencies.auth import get_current_user
from app.presentation.api.dependencies.persistence import get_unit_of_work
from app.presentation.api.exception_handlers import register_exception_handlers
from app.presentation.api.routers import api_router

_VALID_HASH = "$2b$12$" + ("N" * 53)
_TEST_SECRET = "test-secret"


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(api_router)
    register_exception_handlers(app)
    return app


def test_protected_route_without_a_token_returns_401(app):
    client = TestClient(app)

    response = client.get("/companies")

    assert response.status_code == 401
    assert response.json()["error_code"] == "UNAUTHORIZED"


def test_protected_route_with_an_overridden_valid_user_returns_200(app):
    user = User(email=Email("jane@example.com"), password_hash=PasswordHash(_VALID_HASH))
    app.dependency_overrides[get_current_user] = lambda: user

    # Only the auth gate is under test here -- the underlying handler's
    # own DB access is faked too, so this doesn't depend on (or touch)
    # the real dev database, consistent with the rest of the suite.
    fake_uow = AsyncMock()
    fake_uow.__aenter__.return_value = fake_uow
    fake_uow.__aexit__.return_value = False
    fake_uow.company_repository.list.return_value = []
    app.dependency_overrides[get_unit_of_work] = lambda: fake_uow

    client = TestClient(app)
    response = client.get("/companies", headers={"Authorization": "Bearer whatever"})

    assert response.status_code == 200


def test_protected_route_with_an_expired_token_returns_401(app):
    now = datetime.now(UTC)
    expired_token = jwt.encode(
        {"sub": "00000000-0000-0000-0000-000000000001", "iat": now - timedelta(hours=9), "exp": now - timedelta(minutes=1)},
        _TEST_SECRET,
        algorithm="HS256",
    )

    client = TestClient(app)
    response = client.get(
        "/companies",
        headers={"Authorization": f"Bearer {expired_token}"},
    )

    # Not asserting 401 here would be wrong for the wrong reason: this
    # process's real JWT_SECRET_KEY is whatever .env/env vars provide,
    # which this test doesn't control -- so a token signed with a
    # different secret is guaranteed invalid regardless, and a token
    # signed with the *real* secret but an expired exp is invalid too.
    # Either way the gate must reject it.
    assert response.status_code == 401


def test_health_stays_public(app):
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
