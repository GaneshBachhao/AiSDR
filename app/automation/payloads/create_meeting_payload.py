"""
Payload for meeting creation.
"""

from datetime import datetime

from app.automation.payloads.base_payload import (
    BaseAutomationPayload,
)


class CreateMeetingPayload(BaseAutomationPayload):
    """
    Payload used by CreateMeetingHandler.
    """

    conversation_id: int

    meeting_time: datetime