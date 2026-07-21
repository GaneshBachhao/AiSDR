"""
Tests for MimeBuilder.
"""

import base64

from app.integrations.gmail.gmail_models import (
    GmailSendRequest,
)

from app.integrations.gmail.mime_builder import (
    MimeBuilder,
)


def test_build_html_email():

    request = GmailSendRequest(

        to="john@example.com",

        subject="AI SDR",

        html_body="<h1>Hello</h1>",

        text_body="Hello",
    )

    encoded = MimeBuilder.build(request)

    assert isinstance(encoded, str)

    decoded = base64.urlsafe_b64decode(
        encoded
    ).decode()

    assert "To: john@example.com" in decoded

    assert "Subject: AI SDR" in decoded

    assert "multipart/alternative" in decoded

    assert "Content-Type: text/plain" in decoded

    assert "Content-Type: text/html" in decoded


def test_build_without_text():

    request = GmailSendRequest(

        to="john@example.com",

        subject="Test",

        html_body="<b>Hi</b>",
    )

    encoded = MimeBuilder.build(request)

    decoded = base64.urlsafe_b64decode(
        encoded
    ).decode()

    assert "To: john@example.com" in decoded

    assert "Subject: Test" in decoded

    assert "Content-Type: text/html" in decoded