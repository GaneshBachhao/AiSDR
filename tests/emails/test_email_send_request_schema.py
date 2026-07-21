"""
Tests for EmailSendRequest schema.
"""

import pytest
from pydantic import ValidationError

from app.emails.schemas.email_send_request_schema import (
    EmailSendRequest,
)


def test_valid_request():

    request = EmailSendRequest(

        to_email="john@example.com",

        subject="AI SDR",

        html_body="<h1>Hello</h1>",

        text_body="Hello",
    )

    assert request.to_email == "john@example.com"

    assert request.subject == "AI SDR"


def test_text_body_optional():

    request = EmailSendRequest(

        to_email="john@example.com",

        subject="AI SDR",

        html_body="<h1>Hello</h1>",
    )

    assert request.text_body is None


def test_invalid_email():

    with pytest.raises(
        ValidationError,
    ):

        EmailSendRequest(

            to_email="invalid-email",

            subject="AI SDR",

            html_body="<h1>Hello</h1>",
        )