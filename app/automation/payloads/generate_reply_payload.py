"""
Payload for reply generation.
"""

from app.automation.payloads.base_payload import (
    BaseAutomationPayload,
)


class GenerateReplyPayload(BaseAutomationPayload):
    """
    Payload used by GenerateReplyHandler.
    """

    conversation_id: int