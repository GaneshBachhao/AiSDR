"""
AI dependency registrations.
"""

from __future__ import annotations

from app.infrastructure.ai.adapters.application_ai_provider import (
    ApplicationAIProvider,
)
from app.infrastructure.ai.clients import (
    AzureOpenAIClient,
    GeminiClient,
    OllamaClient,
    OpenAIClient,
)
from app.infrastructure.ai.configuration import (
    ProviderSettings,
)
from app.infrastructure.ai.providers import (
    AzureOpenAIProvider,
    GeminiProvider,
    OllamaProvider,
    OpenAIProvider,
)


def create_application_ai_provider(
    settings: ProviderSettings,
) -> ApplicationAIProvider:
    """
    Create the application AI provider.
    """

    return ApplicationAIProvider(
        providers={
            "openai": OpenAIProvider(
                OpenAIClient(settings),
                settings,
            ),
            "azure_openai": AzureOpenAIProvider(
                AzureOpenAIClient(settings),
                settings,
            ),
            "gemini": GeminiProvider(
                GeminiClient(settings),
                settings,
            ),
            "ollama": OllamaProvider(
                OllamaClient(settings),
                settings,
            ),
        },
    )