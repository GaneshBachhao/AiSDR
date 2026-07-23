from abc import ABC, abstractmethod
from typing import Any


class BaseAIClient(ABC):
    """
    Base contract for external AI clients.

    Handles communication with AI provider APIs.
    """


    @abstractmethod
    async def send_request(
        self,
        payload: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Send request to AI provider.

        Returns raw provider response.
        """

        pass


    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check provider availability.
        """

        pass