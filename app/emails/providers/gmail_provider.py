"""
Gmail Email Provider

Concrete implementation of BaseEmailProvider.
"""

from app.emails.providers.base_provider import (
    BaseEmailProvider,
)

from app.emails.schemas.email_schema import (
    EmailCreate,
)

from app.emails.schemas.email_send_result_schema import (
    EmailSendResult,
)

from app.integrations.gmail.gmail_client import (
    GmailClient,
)

from app.integrations.gmail.gmail_models import (
    GmailSendRequest,
)

from app.integrations.gmail.mime_builder import (
    MimeBuilder,
)


class GmailProvider(BaseEmailProvider):
    """
    Gmail implementation of BaseEmailProvider.
    """

    def __init__(
        self,
        client: GmailClient | None = None,
    ):

        self.client = (
            client
            if client is not None
            else GmailClient()
        )

    @property
    def provider_name(self) -> str:

        return "gmail"

    def health_check(
        self,
    ) -> bool:
        """
        Basic provider health check.
        """

        try:

            self.client.auth.get_credentials()

            return True

        except Exception:

            return False

    def send(
        self,
        email: EmailCreate,
    ) -> EmailSendResult:
        """
        Send email using Gmail.
        """

        request = GmailSendRequest(

            # Your EmailCreate currently doesn't have a recipient.
            # We'll replace this with email.to_email in the next sprint.
            to="test@example.com",

            subject=email.subject,

            html_body=email.body,

            text_body=email.body,
        )

        encoded = MimeBuilder.build(
            request,
        )

        response = self.client.send(
            encoded,
        )

        return EmailSendResult(

            success=True,

            provider=self.provider_name,

            message_id=response.message_id,

            thread_id=response.thread_id,
        )