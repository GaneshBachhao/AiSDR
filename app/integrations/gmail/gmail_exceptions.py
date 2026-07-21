"""
Gmail Integration Exceptions

Exceptions raised by the Gmail integration layer.

These exceptions are provider-specific and should
never leak Google SDK exceptions into the rest of
the application.
"""


class GmailException(Exception):
    """
    Base exception for Gmail integration.
    """

    pass


class GmailConfigurationException(GmailException):
    """
    Raised when Gmail configuration
    is missing or invalid.
    """

    pass


class GmailAuthenticationException(GmailException):
    """
    Raised when authentication fails.
    """

    pass


class GmailAuthorizationException(GmailException):
    """
    Raised when the authenticated
    account is not authorized.
    """

    pass


class GmailConnectionException(GmailException):
    """
    Raised when Gmail cannot
    be reached.
    """

    pass


class GmailRateLimitException(GmailException):
    """
    Raised when Gmail API
    rate limits requests.
    """

    pass


class GmailSendException(GmailException):
    """
    Raised when sending an
    email fails.
    """

    pass


class GmailDraftException(GmailException):
    """
    Raised when draft creation
    fails.
    """

    pass


class GmailThreadException(GmailException):
    """
    Raised when thread operations
    fail.
    """

    pass


class GmailMessageNotFoundException(GmailException):
    """
    Raised when a Gmail message
    cannot be found.
    """

    pass


class GmailAttachmentException(GmailException):
    """
    Raised when attachment
    processing fails.
    """

    pass