"""
Tests for Gmail Exceptions.
"""

import pytest

from app.integrations.gmail.gmail_exceptions import (
    GmailException,
    GmailConfigurationException,
    GmailAuthenticationException,
    GmailAuthorizationException,
    GmailConnectionException,
    GmailRateLimitException,
    GmailSendException,
    GmailDraftException,
    GmailThreadException,
    GmailMessageNotFoundException,
    GmailAttachmentException,
)


@pytest.mark.parametrize(
    "exception_class",
    [
        GmailConfigurationException,
        GmailAuthenticationException,
        GmailAuthorizationException,
        GmailConnectionException,
        GmailRateLimitException,
        GmailSendException,
        GmailDraftException,
        GmailThreadException,
        GmailMessageNotFoundException,
        GmailAttachmentException,
    ],
)
def test_all_exceptions_inherit_gmail_exception(
    exception_class,
):

    assert issubclass(
        exception_class,
        GmailException,
    )


def test_exception_message():

    message = "Test Error"

    ex = GmailSendException(message)

    assert str(ex) == message