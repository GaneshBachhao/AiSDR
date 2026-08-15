from __future__ import annotations

from app.infrastructure.configuration.ai_budget_settings import AIBudgetSettings


def test_daily_budget_for_returns_configured_value():
    settings = AIBudgetSettings(ai_daily_request_budget_gemini=20)
    assert settings.daily_budget_for("gemini") == 20


def test_daily_budget_for_case_and_whitespace_insensitive():
    settings = AIBudgetSettings(ai_daily_request_budget_gemini=20)
    assert settings.daily_budget_for(" Gemini ") == 20


def test_daily_budget_for_returns_none_when_zero():
    settings = AIBudgetSettings(ai_daily_request_budget_openai=0)
    assert settings.daily_budget_for("openai") is None


def test_daily_budget_for_returns_none_for_unknown_provider():
    settings = AIBudgetSettings()
    assert settings.daily_budget_for("unknown-provider") is None


def test_gemini_default_matches_known_free_tier_limit():
    assert AIBudgetSettings().ai_daily_request_budget_gemini == 20
