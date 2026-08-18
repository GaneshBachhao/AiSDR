"""
Loads AI configuration from environment variables.
"""

from __future__ import annotations

import os

from .ai_settings import AISettings
from .model_settings import ModelSettings
from .provider_settings import ProviderSettings


class SettingsLoader:
    """
    Loads AI configuration.
    """

    @staticmethod
    def load() -> AISettings:

        provider = os.getenv(
            "AI_PROVIDER",
            "mock",
        ).lower()

        providers = {
            provider: ProviderSettings(
                provider_name=provider,
                api_key=os.getenv(
                    "AI_API_KEY",
                ),
                endpoint=os.getenv(
                    "AI_ENDPOINT",
                ),
                api_version=os.getenv(
                    "AI_API_VERSION",
                ),
                organization_id=os.getenv(
                    "AI_ORGANIZATION_ID",
                ),
                enabled=True,
            ),
        }

        model_name = os.getenv(
            "AI_MODEL",
            "mock-model",
        )

        models = {
            model_name: ModelSettings(
                model_name=model_name,
                max_tokens=int(
                    os.getenv(
                        "AI_MAX_TOKENS",
                        "4096",
                    )
                ),
                temperature=float(
                    os.getenv(
                        "AI_TEMPERATURE",
                        "0.7",
                    )
                ),
            ),
        }

        return AISettings(
            default_provider=provider,
            request_timeout_seconds=int(
                os.getenv(
                    "AI_TIMEOUT",
                    "60",
                )
            ),
            max_retries=int(
                os.getenv(
                    "AI_MAX_RETRIES",
                    "3",
                )
            ),
            enable_streaming=(
                os.getenv(
                    "AI_ENABLE_STREAMING",
                    "false",
                ).lower()
                == "true"
            ),
            providers=providers,
            models=models,
        )
