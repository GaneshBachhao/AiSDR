"""
Email Send Result Schema

Standard response returned by every
email provider after attempting
to send an email.
"""

from pydantic import BaseModel


class EmailSendResult(BaseModel):
    """
    Standard provider response.
    """

    success: bool

    provider: str

    message_id: str | None = None

    thread_id: str | None = None

    error_message: str | None = None