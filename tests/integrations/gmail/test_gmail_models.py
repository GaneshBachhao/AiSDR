"""
Tests for Gmail Models.
"""

from app.integrations.gmail.gmail_models import (
    GmailHealthResponse,
    GmailSendRequest,
    GmailSendResponse,
)


def test_send_request():

    request = GmailSendRequest(

        to="john@example.com",

        subject="Hello",

        html_body="<h1>Hello</h1>",

        text_body="Hello",
    )

    assert request.to == "john@example.com"

    assert request.subject == "Hello"

    assert request.html_body == "<h1>Hello</h1>"

    assert request.text_body == "Hello"


def test_send_response():

    response = GmailSendResponse(

        message_id="msg123",

        thread_id="thread456",
    )

    assert response.message_id == "msg123"

    assert response.thread_id == "thread456"


def test_health_response():

    health = GmailHealthResponse(

        authenticated=True,

        email_address="me@gmail.com",
    )

    assert health.authenticated

    assert health.email_address == "me@gmail.com"