"""
Payload for sending an email.
"""

from app.automation.payloads.base_payload import (
    BaseAutomationPayload,
)


class SendEmailPayload(BaseAutomationPayload):
    """
    Payload used by SendEmailHandler.
    """

    email_id: int