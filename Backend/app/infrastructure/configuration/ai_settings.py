"""
Global AI configuration.
"""

from __future__ import annotations

from dataclasses import dataclass

from .provider_settings import ProviderSettings


@dataclass(frozen=True)
class AISettings:
    """
    Root AI configuration.
    """

    default_provider: str

    providers: dict[str, ProviderSettings]