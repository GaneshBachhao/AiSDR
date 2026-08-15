"""
Loads AI configuration from application settings.
"""

from __future__ import annotations

import os

from .ai_settings import AISettings
from .provider_settings import ProviderSettings


class SettingsLoader:
    """
    Loads provider configuration from environment variables.
    """

    @staticmethod
    def load() -> AISettings:

        providers = {
            "gemini": ProviderSettings(
                provider_name="gemini",
                api_key=os.getenv("GEMINI_API_KEY", ""),
                model=os.getenv(
                    "GEMINI_MODEL",
                    "gemini-2.5-pro",
                ),
            ),
            "openai": ProviderSettings(
                provider_name="openai",
                api_key=os.getenv("OPENAI_API_KEY", ""),
                model=os.getenv(
                    "OPENAI_MODEL",
                    "gpt-4.1",
                ),
            ),
            "azure_openai": ProviderSettings(
                provider_name="azure_openai",
                api_key=os.getenv(
                    "AZURE_OPENAI_API_KEY",
                    "",
                ),
                model=os.getenv(
                    "AZURE_OPENAI_MODEL",
                    "gpt-4.1",
                ),
                endpoint=os.getenv(
                    "AZURE_OPENAI_ENDPOINT",
                    "",
                ),
                api_version=os.getenv(
                    "AZURE_OPENAI_API_VERSION",
                    "2025-01-01-preview",
                ),
            ),
        }

        return AISettings(
            default_provider=os.getenv(
                "DEFAULT_AI_PROVIDER",
                "gemini",
            ),
            providers=providers,
        )