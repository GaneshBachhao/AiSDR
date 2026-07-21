
"""
Tests for EmailDispatchService.
"""

from app.emails.schemas.email_send_result_schema import (
    EmailSendResult,
)

from app.emails.services.email_dispatch_service import (
    EmailDispatchService,
)


class FakeProvider:
    def send(
        self,
        request,
    ):

        return EmailSendResult(
            success=True,
            provider="gmail",
            message_id="msg123",
            thread_id="thread456",
        )


class FakeEmailService:
    """
    Prevents database access during unit tests.
    """

    def mark_sending(
        self,
        db,
        email,
    ):
        return email

    def mark_sent(
        self,
        db,
        email,
        provider_message_id,
    ):
        return email

    def mark_failed(
        self,
        db,
        email,
    ):
        return email


class FakeEmail:

    subject = "AI SDR"

    body = "Hello"


class FakeContact:

    email = "john@example.com"


def test_dispatch(monkeypatch):

    monkeypatch.setattr(
        "app.emails.services.email_dispatch_service.EmailProviderFactory.create",
        lambda: FakeProvider(),
    )

    service = EmailDispatchService()

    # Replace the real EmailService
    service.email_service = FakeEmailService()

    result = service.dispatch(
        db=None,
        email=FakeEmail(),
        contact=FakeContact(),
    )

    assert result.success

    assert result.provider == "gmail"

    assert result.message_id == "msg123"

    assert result.thread_id == "thread456"
