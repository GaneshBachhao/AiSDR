"""
Payload for scheduling follow-up.
"""

from datetime import datetime

from app.automation.payloads.base_payload import (
    BaseAutomationPayload,
)


class ScheduleFollowUpPayload(BaseAutomationPayload):
    """
    Payload used by ScheduleFollowUpHandler.
    """

    lead_id: int

    scheduled_at: datetime