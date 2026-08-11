"""
Base AI client contract.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any


class BaseAIClient(ABC):
    """
    Base contract for all AI infrastructure clients.

    Clients are responsible only for communicating
    with external AI services.

    They return the raw provider response.
    """

    @abstractmethod
    async def send_request(
        self,
        payload: dict[str, Any],
    ) -> Any:
        """
        Send a request to the external AI provider.

        Returns the raw provider-specific response.
        """
        raise NotImplementedError

    @abstractmethod
    async def health_check(
        self,
    ) -> bool:
        """
        Verify the AI provider is available.
        """
        raise NotImplementedError