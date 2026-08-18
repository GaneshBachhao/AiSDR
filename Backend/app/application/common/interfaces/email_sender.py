"""
Email sender application port.

Infrastructure provides actual email delivery.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class EmailSender(ABC):
    """
    Contract for sending emails.
    """

    @abstractmethod
    async def send(
        self,
        *,
        recipient: str,
        subject: str,
        body: str,
    ) -> None:
        """
        Send an email.
        """
        raise NotImplementedError
