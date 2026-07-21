"""
MIME Builder

Builds RFC822 MIME email messages for Gmail.
"""

import base64

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.integrations.gmail.gmail_models import (
    GmailSendRequest,
)


class MimeBuilder:
    """
    Builds MIME messages compatible with Gmail.
    """

    @staticmethod
    def build(
        request: GmailSendRequest,
    ) -> str:
        """
        Build and encode a MIME message.

        Returns:
            Base64 URL-safe encoded MIME string.
        """

        message = MIMEMultipart(
            "alternative"
        )

        message["To"] = request.to

        message["Subject"] = request.subject

        if request.text_body:

            message.attach(

                MIMEText(
                    request.text_body,
                    "plain",
                    "utf-8",
                )
            )

        message.attach(

            MIMEText(
                request.html_body,
                "html",
                "utf-8",
            )
        )

        encoded = base64.urlsafe_b64encode(

            message.as_bytes()

        ).decode()

        return encoded