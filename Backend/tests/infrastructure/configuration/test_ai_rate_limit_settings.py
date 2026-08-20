from __future__ import annotations

from app.infrastructure.configuration.ai_rate_limit_settings import AIRateLimitSettings


def test_rpm_for_returns_configured_value():
    settings = AIRateLimitSettings(ai_rate_limit_rpm_gemini=5)
    assert settings.rpm_for("gemini") == 5


def test_rpm_for_case_and_whitespace_insensitive():
    settings = AIRateLimitSettings(ai_rate_limit_rpm_gemini=5)
    assert settings.rpm_for(" Gemini ") == 5


def test_rpm_for_returns_none_when_zero():
    settings = AIRateLimitSettings(ai_rate_limit_rpm_openai=0)
    assert settings.rpm_for("openai") is None


def test_rpm_for_returns_none_for_unknown_provider():
    settings = AIRateLimitSettings()
    assert settings.rpm_for("unknown-provider") is None


def test_gemini_default_matches_known_free_tier_rpm_limit():
    assert AIRateLimitSettings().ai_rate_limit_rpm_gemini == 5
