"""
Tests for GmailClient.
"""

from unittest.mock import MagicMock

from app.integrations.gmail.gmail_client import (
    GmailClient,
)

from app.integrations.gmail.gmail_models import (
    GmailSendResponse,
)


class FakeAuth:

    def get_credentials(self):

        return object()


def test_send_email(
    monkeypatch,
):

    fake_execute = MagicMock(
        return_value={
            "id": "msg123",
            "threadId": "thread456",
        }
    )

    fake_send = MagicMock()
    fake_send.execute = fake_execute

    fake_messages = MagicMock()
    fake_messages.send.return_value = fake_send

    fake_users = MagicMock()
    fake_users.messages.return_value = fake_messages

    fake_service = MagicMock()
    fake_service.users.return_value = fake_users

    monkeypatch.setattr(
        "app.integrations.gmail.gmail_client.build",
        lambda *args, **kwargs: fake_service,
    )

    client = GmailClient(
        auth=FakeAuth(),
    )

    response = client.send(
        "encoded-message"
    )

    assert isinstance(
        response,
        GmailSendResponse,
    )

    assert (
        response.message_id
        == "msg123"
    )

    assert (
        response.thread_id
        == "thread456"
    )