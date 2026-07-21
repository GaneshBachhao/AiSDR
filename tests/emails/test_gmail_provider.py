"""
Tests for GmailProvider.
"""

from app.emails.providers.gmail_provider import (
    GmailProvider,
)

from app.emails.schemas.email_schema import (
    EmailCreate,
)

from app.emails.schemas.email_send_result_schema import (
    EmailSendResult,
)

from app.integrations.gmail.gmail_models import (
    GmailSendResponse,
)


class FakeClient:

    def send(
        self,
        encoded_message: str,
    ):

        return GmailSendResponse(

            message_id="msg123",

            thread_id="thread456",
        )


def test_send_email():

    provider = GmailProvider(

        client=FakeClient(),
    )

    email = EmailCreate(

        lead_id=1,

        subject="AI SDR",

        body="Hello",

        provider="gmail",
    )

    result = provider.send(
        email,
    )

    assert isinstance(
        result,
        EmailSendResult,
    )

    assert result.success is True

    assert result.provider == "gmail"

    assert result.message_id == "msg123"

    assert result.thread_id == "thread456"