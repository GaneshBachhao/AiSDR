"""
Gmail Models

Internal models used by the Gmail integration.

These models isolate Google-specific request and
response data from the rest of the application.
"""

from pydantic import BaseModel


# ==========================================================
# Request
# ==========================================================


class GmailSendRequest(BaseModel):
    """
    Gmail send request.
    """

    to: str

    subject: str

    html_body: str

    text_body: str | None = None


# ==========================================================
# Response
# ==========================================================


class GmailSendResponse(BaseModel):
    """
    Gmail send response.
    """

    message_id: str

    thread_id: str


# ==========================================================
# Health Check
# ==========================================================


class GmailHealthResponse(BaseModel):
    """
    Gmail health check response.
    """

    authenticated: bool

    email_address: str | None = None