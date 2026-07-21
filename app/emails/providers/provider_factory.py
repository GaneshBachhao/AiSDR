"""
Email Provider Factory

Returns the configured email provider.

Currently only Gmail is supported.
"""

from app.emails.providers.base_provider import (
    BaseEmailProvider,
)

from app.emails.providers.gmail_provider import (
    GmailProvider,
)


class EmailProviderFactory:
    """
    Creates email providers.
    """

    @staticmethod
    def create() -> BaseEmailProvider:
        """
        Returns the default email provider.

        Currently Gmail is the only supported
        provider.
        """

        return GmailProvider()