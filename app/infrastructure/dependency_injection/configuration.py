"""
Dependency Injection - Configuration.
"""

from __future__ import annotations

from app.infrastructure.ai.configuration import (
    AISettings,
    ModelSettings,
    ProviderSettings,
)


class Configuration:
    """
    Creates application configuration objects.
    """

    @staticmethod
    def ai_settings() -> AISettings:
        return AISettings()

    @staticmethod
    def provider_settings() -> ProviderSettings:
        return ProviderSettings(
            provider_name="mock",
            enabled=True,
        )

    @staticmethod
    def model_settings() -> ModelSettings:
        return ModelSettings(
            model_name="mock-model",
        )