"""
Email Dispatch Service

Coordinates outbound email delivery.
"""

from sqlalchemy.orm import Session

from app.emails.providers.provider_factory import (
    EmailProviderFactory,
)

from app.emails.schemas.email_send_request_schema import (
    EmailSendRequest,
)

from app.emails.schemas.email_send_result_schema import (
    EmailSendResult,
)

from app.emails.services.email_service import (
    EmailService,
)

from app.models.contact import Contact
from app.models.email import Email


class EmailDispatchService:
    """
    Dispatches outbound emails through the configured provider.
    """

    def __init__(
        self,
        email_service: EmailService | None = None,
    ):

        self.provider = (
            EmailProviderFactory.get_provider()
        )

        self.email_service = (
            email_service
            if email_service is not None
            else EmailService()
        )

    def dispatch(
        self,
        db: Session,
        email: Email,
        contact: Contact,
    ) -> EmailSendResult:
        """
        Sends an email and updates its lifecycle.
        """

        request = EmailSendRequest(
            to_email=contact.email,
            subject=email.subject,
            html_body=email.body,
            text_body=email.body,
        )

        result = self.provider.send(
            request,
        )

        if result.success:

            self.email_service.mark_sent(
                db,
                email,
                provider_message_id=result.message_id or "",
            )

        else:

            self.email_service.mark_failed(
                db,
                email,
            )

        return result