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

import os
from dataclasses import dataclass

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
from app.infrastructure.ai.usage.ai_budget_guard import AIBudgetGuard
from app.infrastructure.ai.usage.ai_rate_limiter import AIRateLimiter
from app.infrastructure.ai.usage.ai_usage_tracker import AIUsageTracker
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
        "azure_openai": AzureOpenAIProvider(AzureOpenAIClient(azure_openai_settings), azure_openai_settings),
    }


def build_ai_execution_service() -> AIExecutionService:
    """Assemble an ``AIExecutionService`` backed by every configured provider.

    Wires the ``AI_PROVIDER_FALLBACK`` setting through so a recoverable
    failure on the primary provider (deprecated model, exhausted quota)
    automatically retries against the next configured provider instead of
    failing the whole request. Every call (success or failure) is logged
    via ``AIUsageTracker`` for budget tracking -- see ``build_ai_budget_guard``.
    Also wires the shared ``AIRateLimiter`` singleton (see
    ``get_ai_rate_limiter``) so concurrent fan-out can't burst past a
    provider's per-minute limit even though this function itself builds a
    fresh ``ApplicationAIProvider`` on every call.
    """

    providers = build_ai_providers()
    fallback_settings = AIProviderSettings()
    default_models = {name: default_model_for_provider(name) for name in providers}

    application_provider = ApplicationAIProvider(
        providers=providers,
        fallback_order=fallback_settings.fallback_list(),
        default_models=default_models,
        rate_limiter=get_ai_rate_limiter(),
    )
    return AIExecutionService(
        application_provider,
        usage_recorder=AIUsageTracker(),
    )


def build_ai_budget_guard() -> AIBudgetGuard:
    """Assemble an ``AIBudgetGuard`` backed by the same usage log."""

    return AIBudgetGuard(tracker=AIUsageTracker())


# Loaded once, at process scope, same singleton pattern as
# get_directory_adapter (app/presentation/api/dependencies/company_research.py)
# -- unlike AIBudgetGuard (state lives in the DB, safe to rebuild per
# request), an in-process RPM limiter's state (recent call timestamps) must
# survive across requests and across one request's concurrent fan-out, or
# it limits nothing.
_ai_rate_limiter: AIRateLimiter | None = None


def get_ai_rate_limiter() -> AIRateLimiter:
    global _ai_rate_limiter
    if _ai_rate_limiter is None:
        _ai_rate_limiter = AIRateLimiter()
    return _ai_rate_limiter


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


@dataclass(frozen=True)
class ProviderDiagnostics:
    """Effective, secret-safe configuration snapshot for one AI provider."""

    provider: str
    configured: bool
    model: str
    key_fingerprint: str | None
    key_source: str  # "environment_variable" | "dotenv_file" | "not_set"


def _key_fingerprint(api_key: str) -> str | None:
    if not api_key:
        return None
    return f"***{api_key[-4:]}" if len(api_key) >= 4 else "***"


def _key_source(env_var_name: str, resolved_value: str) -> str:
    if not resolved_value:
        return "not_set"
    # pydantic-settings never writes .env values back into os.environ, so a
    # real hit here means a genuine process/OS-level environment variable is
    # shadowing (or supplying) the value -- exactly the failure mode that
    # took several manual os.environ inspections to diagnose previously.
    if env_var_name in os.environ:
        return "environment_variable"
    return "dotenv_file"


def ai_config_diagnostics() -> list[ProviderDiagnostics]:
    """Effective AI provider configuration, with secrets redacted.

    Reports, per provider: whether it's usable, which model it will call,
    a last-4-characters key fingerprint (never the full key), and whether
    the key came from a real environment variable or only from ``.env`` --
    so a shadowing env var is visible in one call instead of a manual
    ``os.environ`` investigation.
    """

    gemini = GeminiSettings()
    openai = OpenAISettings()
    azure = AzureOpenAISettings()

    return [
        ProviderDiagnostics(
            provider="gemini",
            configured=bool(gemini.gemini_api_key),
            model=gemini.gemini_model,
            key_fingerprint=_key_fingerprint(gemini.gemini_api_key),
            key_source=_key_source("GEMINI_API_KEY", gemini.gemini_api_key),
        ),
        ProviderDiagnostics(
            provider="openai",
            configured=bool(openai.openai_api_key),
            model=openai.openai_model,
            key_fingerprint=_key_fingerprint(openai.openai_api_key),
            key_source=_key_source("OPENAI_API_KEY", openai.openai_api_key),
        ),
        ProviderDiagnostics(
            provider="azure_openai",
            configured=bool(azure.azure_openai_api_key and azure.azure_openai_endpoint),
            model=azure.azure_openai_model,
            key_fingerprint=_key_fingerprint(azure.azure_openai_api_key),
            key_source=_key_source("AZURE_OPENAI_API_KEY", azure.azure_openai_api_key),
        ),
    ]
