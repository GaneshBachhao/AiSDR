"""
Gmail Client

Low-level Gmail API client responsible for
sending MIME messages through Gmail.
"""

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.integrations.gmail.gmail_auth import GmailAuth
from app.integrations.gmail.gmail_exceptions import (
    GmailAuthenticationException,
    GmailSendException,
)
from app.integrations.gmail.gmail_models import (
    GmailSendResponse,
)


class GmailClient:
    """
    Gmail API client.
    """

    def __init__(
        self,
        auth: GmailAuth | None = None,
    ):

        self.auth = auth if auth else GmailAuth()

    # ======================================================
    # Public
    # ======================================================

    def send(
        self,
        encoded_message: str,
    ) -> GmailSendResponse:
        """
        Send a MIME email through Gmail.

        Args:
            encoded_message:
                Base64 URL-safe MIME message.

        Returns:
            GmailSendResponse
        """

        try:

            credentials = (
                self.auth.get_credentials()
            )

            service = build(
                "gmail",
                "v1",
                credentials=credentials,
            )

            response = (
                service.users()
                .messages()
                .send(
                    userId="me",
                    body={
                        "raw": encoded_message,
                    },
                )
                .execute()
            )

            return GmailSendResponse(

                message_id=response["id"],

                thread_id=response["threadId"],
            )

        except HttpError as ex:

            raise GmailSendException(
                str(ex)
            ) from ex

        except Exception as ex:

            raise GmailAuthenticationException(
                str(ex)
            ) from ex