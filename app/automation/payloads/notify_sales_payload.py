"""
Payload for notifying Sales.
"""

from app.automation.payloads.base_payload import (
    BaseAutomationPayload,
)


class NotifySalesPayload(BaseAutomationPayload):
    """
    Payload used by NotifySalesHandler.
    """

    lead_id: int

    message: str