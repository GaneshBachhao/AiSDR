"""
Provider-specific AI configuration.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderSettings:
    """
    Configuration for a single AI provider.
    """

    provider_name: str

    api_key: str | None = None

    endpoint: str | None = None

    api_version: str | None = None

    organization_id: str | None = None

    enabled: bool = True

    def __post_init__(self) -> None:

        provider = self.provider_name.strip().lower()

        if not provider:
            raise ValueError("Provider name is required.")

        object.__setattr__(
            self,
            "provider_name",
            provider,
        )

        if self.enabled and provider != "mock" and not self.api_key:
            raise ValueError("API key is required for enabled providers.")

    @property
    def is_mock_provider(
        self,
    ) -> bool:
        return self.provider_name == "mock"
