"""
Gmail Authentication

Handles OAuth authentication and credential
management for the Gmail API.
"""

from pathlib import Path

from google.auth.transport.requests import Request

from google.oauth2.credentials import Credentials

from google_auth_oauthlib.flow import InstalledAppFlow

from app.core.config import settings

from app.integrations.gmail.gmail_exceptions import (
    GmailAuthenticationException,
)


class GmailAuth:
    """
    Gmail OAuth authentication helper.
    """

    def __init__(self):

        self.token_file = Path(
            settings.GOOGLE_TOKEN_FILE
        )

        self.credentials_file = Path(
            settings.GOOGLE_CREDENTIALS_FILE
        )

        self.scopes = settings.GOOGLE_SCOPES

    # ======================================================
    # Public
    # ======================================================

    def get_credentials(
        self,
    ) -> Credentials:
        """
        Returns valid Gmail credentials.
        """

        credentials = self._load_credentials()

        if credentials:

            if credentials.valid:

                return credentials

            if (
                credentials.expired
                and credentials.refresh_token
            ):

                credentials.refresh(
                    Request(),
                )

                self._save_credentials(
                    credentials,
                )

                return credentials

        return self._authenticate()

    # ======================================================
    # Private
    # ======================================================

    def _load_credentials(
        self,
    ) -> Credentials | None:

        if not self.token_file.exists():

            return None

        return Credentials.from_authorized_user_file(

            str(
                self.token_file,
            ),

            self.scopes,
        )

    def _save_credentials(
        self,
        credentials: Credentials,
    ) -> None:

        self.token_file.write_text(

            credentials.to_json(),

            encoding="utf-8",
        )

    def _authenticate(
        self,
    ) -> Credentials:

        if not self.credentials_file.exists():

            raise GmailAuthenticationException(

                f"Credentials file not found: "
                f"{self.credentials_file}"
            )

        flow = (
            InstalledAppFlow
            .from_client_secrets_file(

                str(
                    self.credentials_file,
                ),

                self.scopes,
            )
        )

        credentials = flow.run_local_server(

            port=0,
        )

        self._save_credentials(
            credentials,
        )

        return credentials