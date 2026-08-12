from __future__ import annotations

import pytest

from app.infrastructure.ai.composition import (
    build_ai_execution_service,
    build_ai_providers,
    build_azure_openai_provider_settings,
    build_gemini_provider_settings,
    build_openai_provider_settings,
    default_ai_provider,
    default_model_for_provider,
)
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
