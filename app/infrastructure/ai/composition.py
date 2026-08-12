"""
Composition helpers for the AI infrastructure.

Bridges the centralized application settings
(``app.infrastructure.configuration``) to the AI provider/client
contracts in this package, and assembles a ready-to-use, multi-provider
``AIExecutionService``. This is the one shared entry point other modules
should depend on to get a working AI provider, instead of constructing
providers/clients by hand.

Every supported provider (Gemini, OpenAI, Azure OpenAI) is registered
regardless of whether it currently has real credentials configured -- an
unconfigured provider's client raises a clear ``AIClientException`` on
first use rather than being silently absent from routing. Callers select
a provider per request via ``AIRequest.provider``.
"""

from __future__ import annotations

from app.application.ai.services.ai_execution_service import AIExecutionService
from app.infrastructure.ai.adapters.application_ai_provider import ApplicationAIProvider
from app.infrastructure.ai.clients.azure_openai_client import AzureOpenAIClient
from app.infrastructure.ai.clients.gemini_client import GeminiClient
from app.infrastructure.ai.clients.openai_client import OpenAIClient
from app.infrastructure.ai.configuration import ProviderSettings
from app.infrastructure.ai.providers.azure_openai_provider import AzureOpenAIProvider
from app.infrastructure.ai.providers.base_provider import BaseAIProvider
from app.infrastructure.ai.providers.gemini_provider import GeminiProvider
from app.infrastructure.ai.providers.openai_provider import OpenAIProvider
from app.infrastructure.configuration.ai_provider_settings import AIProviderSettings
from app.infrastructure.configuration.azure_openai_settings import AzureOpenAISettings
from app.infrastructure.configuration.gemini_settings import GeminiSettings
from app.infrastructure.configuration.openai_settings import OpenAISettings


def build_gemini_provider_settings(
    settings: GeminiSettings | None = None,
) -> ProviderSettings:
    """Build the AI-infrastructure ``ProviderSettings`` for Gemini."""

    resolved = settings or GeminiSettings()
    key = resolved.gemini_api_key

    return ProviderSettings(
        provider_name="gemini",
        api_key=key or None,
        enabled=bool(key),
    )


def build_openai_provider_settings(
    settings: OpenAISettings | None = None,
) -> ProviderSettings:
    """Build the AI-infrastructure ``ProviderSettings`` for OpenAI."""

    resolved = settings or OpenAISettings()
    key = resolved.openai_api_key

    return ProviderSettings(
        provider_name="openai",
        api_key=key or None,
        enabled=bool(key),
    )


def build_azure_openai_provider_settings(
    settings: AzureOpenAISettings | None = None,
) -> ProviderSettings:
    """Build the AI-infrastructure ``ProviderSettings`` for Azure OpenAI."""

    resolved = settings or AzureOpenAISettings()
    key = resolved.azure_openai_api_key
    configured = bool(key and resolved.azure_openai_endpoint)

    return ProviderSettings(
        provider_name="azure_openai",
        api_key=key or None,
        endpoint=resolved.azure_openai_endpoint or None,
        api_version=resolved.azure_openai_api_version or None,
        enabled=configured,
    )


def build_ai_providers() -> dict[str, BaseAIProvider]:
    """Build every supported AI provider, keyed by provider name."""

    gemini_settings = build_gemini_provider_settings()
    openai_settings = build_openai_provider_settings()
    azure_openai_settings = build_azure_openai_provider_settings()

    return {
        "gemini": GeminiProvider(GeminiClient(gemini_settings), gemini_settings),
        "openai": OpenAIProvider(OpenAIClient(openai_settings), openai_settings),
        "azure_openai": AzureOpenAIProvider(
            AzureOpenAIClient(azure_openai_settings), azure_openai_settings
        ),
    }


def build_ai_execution_service() -> AIExecutionService:
    """Assemble an ``AIExecutionService`` backed by every configured provider."""

    application_provider = ApplicationAIProvider(providers=build_ai_providers())
    return AIExecutionService(application_provider)


def default_ai_provider() -> str:
    """Return the application-wide default AI provider name (``AI_PROVIDER`` in .env).

    This is the single source of truth for provider selection across the
    app -- individual modules should call this instead of defining their
    own provider-selection setting.
    """

    return AIProviderSettings().ai_provider


def default_model_for_provider(provider_name: str) -> str:
    """Return the configured default model/deployment name for a provider."""

    normalized = provider_name.strip().lower()
    if normalized == "gemini":
        return GeminiSettings().gemini_model
    if normalized == "openai":
        return OpenAISettings().openai_model
    if normalized == "azure_openai":
        return AzureOpenAISettings().azure_openai_model
    raise ValueError(f"No default model configured for provider '{provider_name}'.")
