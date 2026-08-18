"""
Tests for ExceptionMiddleware.

Regression guard: the middleware's catch-and-format block used to be
commented out entirely, so any exception with no registered
`ApplicationException` handler (a raw IntegrityError, an
AIProviderException, a bug) propagated all the way to Starlette's
default error response instead of this app's normal
`{success, message, error_code, details}` shape.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.presentation.api.exception_handlers import register_exception_handlers
from app.presentation.api.middleware.exception import ExceptionMiddleware


def _make_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(ExceptionMiddleware)
    register_exception_handlers(app)

    @app.get("/boom")
    async def boom():
        raise ValueError("something broke")

    @app.get("/not-found")
    async def not_found():
        raise NotFoundException(message="Thing not found.", details={"id": "123"})

    return app


def test_an_unregistered_exception_returns_a_structured_500_not_a_raw_traceback():
    client = TestClient(_make_app(), raise_server_exceptions=False)

    response = client.get("/boom")

    assert response.status_code == 500
    body = response.json()
    assert body["success"] is False
    assert body["message"] == "Internal Server Error"
    assert body["error_code"] == "INTERNAL_ERROR"
    assert body["details"] == {}


def test_an_application_exception_still_gets_its_own_status_code_not_swallowed_as_500():
    client = TestClient(_make_app(), raise_server_exceptions=False)

    response = client.get("/not-found")

    assert response.status_code == 404
    body = response.json()
    assert body["error_code"] == "NOT_FOUND"
    assert body["message"] == "Thing not found."
