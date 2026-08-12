from __future__ import annotations

import pytest

from app.infrastructure.ai.composition import (
    ai_config_diagnostics,
    build_ai_budget_guard,
    build_ai_execution_service,
    build_ai_providers,
    build_azure_openai_provider_settings,
    build_gemini_provider_settings,
    build_openai_provider_settings,
    default_ai_provider,
    default_model_for_provider,
)
from app.infrastructure.ai.usage.ai_budget_guard import AIBudgetGuard
from app.infrastructure.configuration.ai_provider_settings import AIProviderSettings
from app.infrastructure.configuration.azure_openai_settings import AzureOpenAISettings
from app.infrastructure.configuration.gemini_settings import GeminiSettings
from app.infrastructure.configuration.openai_settings import OpenAISettings


def test_build_ai_providers_registers_all_three():
    providers = build_ai_providers()
    assert set(providers.keys()) == {"gemini", "openai", "azure_openai"}


def test_build_ai_execution_service_builds_without_error():
    service = build_ai_execution_service()
    assert service is not None


def test_gemini_provider_settings_disabled_without_key():
    settings = build_gemini_provider_settings(GeminiSettings(gemini_api_key=""))
    assert settings.enabled is False


def test_openai_provider_settings_enabled_with_key():
    settings = build_openai_provider_settings(OpenAISettings(openai_api_key="secret"))
    assert settings.enabled is True
    assert settings.api_key == "secret"


def test_azure_openai_provider_settings_requires_endpoint_and_key():
    only_key = build_azure_openai_provider_settings(
        AzureOpenAISettings(azure_openai_api_key="secret", azure_openai_endpoint="")
    )
    assert only_key.enabled is False

    fully_configured = build_azure_openai_provider_settings(
        AzureOpenAISettings(
            azure_openai_api_key="secret",
            azure_openai_endpoint="https://example.openai.azure.com",
        )
    )
    assert fully_configured.enabled is True
    assert fully_configured.endpoint == "https://example.openai.azure.com"


def test_default_model_for_provider_covers_all_three():
    assert default_model_for_provider("gemini") == GeminiSettings().gemini_model
    assert default_model_for_provider("openai") == OpenAISettings().openai_model
    assert default_model_for_provider("azure_openai") == AzureOpenAISettings().azure_openai_model


def test_default_model_for_provider_raises_for_unknown_provider():
    with pytest.raises(ValueError, match="No default model"):
        default_model_for_provider("unknown-provider")


def test_default_ai_provider_reads_the_single_app_wide_setting():
    assert default_ai_provider() == AIProviderSettings().ai_provider


def test_fallback_list_parses_comma_separated_env_value(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER_FALLBACK", "openai, azure_openai ,openai")
    assert AIProviderSettings().fallback_list() == [
        "openai",
        "azure_openai",
        "openai",
    ]


def test_fallback_list_empty_by_default(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER_FALLBACK", "")
    assert AIProviderSettings().fallback_list() == []


def test_build_ai_execution_service_wires_configured_fallback(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER_FALLBACK", "openai")

    service = build_ai_execution_service()

    provider = service._provider  # noqa: SLF001 -- white-box wiring check
    assert provider._fallback_order == ["openai"]
    assert provider._default_models["openai"] == OpenAISettings().openai_model


def test_ai_config_diagnostics_covers_all_three_providers():
    diagnostics = {d.provider: d for d in ai_config_diagnostics()}
    assert set(diagnostics) == {"gemini", "openai", "azure_openai"}


def test_ai_config_diagnostics_masks_key_and_flags_env_var_source(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "abcd-1234-ZZZZ")

    diagnostics = {d.provider: d for d in ai_config_diagnostics()}
    gemini = diagnostics["gemini"]

    assert gemini.configured is True
    assert gemini.key_fingerprint == "***ZZZZ"
    assert gemini.key_source == "environment_variable"


def test_ai_config_diagnostics_reports_not_set_when_no_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "")

    diagnostics = {d.provider: d for d in ai_config_diagnostics()}
    openai_diagnostics = diagnostics["openai"]

    assert openai_diagnostics.configured is False
    assert openai_diagnostics.key_fingerprint is None
    assert openai_diagnostics.key_source == "not_set"


def test_build_ai_execution_service_wires_a_usage_recorder():
    service = build_ai_execution_service()
    assert service._usage_recorder is not None  # noqa: SLF001


def test_build_ai_budget_guard_returns_a_working_guard():
    guard = build_ai_budget_guard()
    assert isinstance(guard, AIBudgetGuard)


def test_ai_config_diagnostics_never_exposes_the_full_key(monkeypatch):
    secret = "sk-super-secret-value-should-never-leak"
    monkeypatch.setenv("OPENAI_API_KEY", secret)

    diagnostics = {d.provider: d for d in ai_config_diagnostics()}

    assert secret not in repr(diagnostics["openai"])
    assert diagnostics["openai"].key_fingerprint == "***leak"
