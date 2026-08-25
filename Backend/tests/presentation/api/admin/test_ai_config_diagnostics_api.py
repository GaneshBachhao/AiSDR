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
    monkeypatch.setenv("GEMINI_API_KEY_2", "")
    monkeypatch.setenv("OPENAI_API_KEY", "")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "")
    monkeypatch.setenv("OPENROUTER_API_KEY", "")

    response = client.get("/admin/ai-config")

    assert response.status_code == 200
    body = response.json()

    assert body["default_provider"] == "gemini"
    assert body["fallback_order"] == ["openai"]

    providers = {p["provider"]: p for p in body["providers"]}
    assert set(providers) == {"gemini", "openai", "azure_openai", "openrouter"}

    assert providers["gemini"]["configured"] is True
    assert providers["gemini"]["key_fingerprint"] == "***WXYZ"
    assert providers["gemini"]["key_source"] == "environment_variable"
    assert providers["gemini"]["second_key_configured"] is False

    assert providers["openai"]["configured"] is False
    assert providers["openai"]["key_fingerprint"] is None
    assert providers["openai"]["key_source"] == "not_set"


def test_reports_second_gemini_key_when_configured(client, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "primary-key-ABCD")
    monkeypatch.setenv("GEMINI_API_KEY_2", "secondary-key-EFGH")

    response = client.get("/admin/ai-config")

    providers = {p["provider"]: p for p in response.json()["providers"]}
    assert providers["gemini"]["second_key_configured"] is True


def test_reports_openrouter_when_configured(client, monkeypatch):
    monkeypatch.setenv("AI_PROVIDER_FALLBACK", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-real-key-ABCD")

    response = client.get("/admin/ai-config")
    body = response.json()

    assert body["fallback_order"] == ["openrouter"]
    providers = {p["provider"]: p for p in body["providers"]}
    assert providers["openrouter"]["configured"] is True
    assert providers["openrouter"]["key_fingerprint"] == "***ABCD"


def test_full_api_key_never_appears_in_the_response_body(client, monkeypatch):
    secret = "sk-super-secret-value-should-never-leak-ABCD"
    monkeypatch.setenv("OPENAI_API_KEY", secret)

    response = client.get("/admin/ai-config")

    assert secret not in response.text
