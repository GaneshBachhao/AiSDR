"""
Tests for GET /admin/ai-config
"""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.presentation.api.routers.admin_router import router


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


def test_returns_all_three_providers_with_expected_shape(client, monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "gemini")
    monkeypatch.setenv("AI_PROVIDER_FALLBACK", "openai")
    monkeypatch.setenv("GEMINI_API_KEY", "gm-secret-key-WXYZ")
    monkeypatch.setenv("OPENAI_API_KEY", "")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "")

    response = client.get("/admin/ai-config")

    assert response.status_code == 200
    body = response.json()

    assert body["default_provider"] == "gemini"
    assert body["fallback_order"] == ["openai"]

    providers = {p["provider"]: p for p in body["providers"]}
    assert set(providers) == {"gemini", "openai", "azure_openai"}

    assert providers["gemini"]["configured"] is True
    assert providers["gemini"]["key_fingerprint"] == "***WXYZ"
    assert providers["gemini"]["key_source"] == "environment_variable"

    assert providers["openai"]["configured"] is False
    assert providers["openai"]["key_fingerprint"] is None
    assert providers["openai"]["key_source"] == "not_set"


def test_full_api_key_never_appears_in_the_response_body(client, monkeypatch):
    secret = "sk-super-secret-value-should-never-leak-ABCD"
    monkeypatch.setenv("OPENAI_API_KEY", secret)

    response = client.get("/admin/ai-config")

    assert secret not in response.text
