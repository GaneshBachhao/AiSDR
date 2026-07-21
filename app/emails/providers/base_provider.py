"""
Base Email Provider

Every email provider must implement
this contract.
"""

from abc import ABC
from abc import abstractmethod

from app.emails.schemas.email_schema import (
    EmailCreate,
)

from app.emails.schemas.email_send_result_schema import (
    EmailSendResult,
)


class BaseEmailProvider(ABC):
    """
    Base email provider contract.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Provider name.
        """

    @abstractmethod
    def send(
        self,
        email: EmailCreate,
    ) -> EmailSendResult:
        """
        Sends an email.
        """

    @abstractmethod
    def health_check(
        self,
    ) -> bool:
        """
        Checks provider availability.
        """