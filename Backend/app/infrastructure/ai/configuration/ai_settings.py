"""
Root AI configuration.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .model_settings import ModelSettings
from .provider_settings import ProviderSettings


@dataclass(frozen=True)
class AISettings:
    """
    Root configuration object for the AI subsystem.
    """

    default_provider: str = "openai"

    request_timeout_seconds: int = 60

    max_retries: int = 3

    enable_streaming: bool = False

    providers: dict[
        str,
        ProviderSettings,
    ] = field(
        default_factory=dict,
    )

    models: dict[
        str,
        ModelSettings,
    ] = field(
        default_factory=dict,
    )

    def __post_init__(self) -> None:

        provider = self.default_provider.strip().lower()

        object.__setattr__(
            self,
            "default_provider",
            provider,
        )

        if self.request_timeout_seconds <= 0:
            raise ValueError("Invalid timeout.")

        if self.max_retries < 0:
            raise ValueError("Invalid retry count.")

        if provider not in self.providers:
            raise ValueError(f"Default provider '{provider}' is not configured.")

    def get_provider(
        self,
        provider_name: str,
    ) -> ProviderSettings:

        try:
            return self.providers[provider_name.lower()]
        except KeyError as ex:
            raise ValueError(f"Provider '{provider_name}' not configured.") from ex

    def get_model(
        self,
        model_name: str,
    ) -> ModelSettings:

        try:
            return self.models[model_name]
        except KeyError as ex:
            raise ValueError(f"Model '{model_name}' not configured.") from ex
