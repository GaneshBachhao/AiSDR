"""
Configuration for a single AI provider.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderSettings:
    """
    Settings for an individual AI provider.
    """

    provider_name: str

    api_key: str

    model: str

    endpoint: str | None = None

    api_version: str | None = None

    timeout: int = 60

    max_retries: int = 3
