"""
Payload for updating a Lead.
"""

from app.automation.payloads.base_payload import (
    BaseAutomationPayload,
)

from app.leads.enums.lead_status import (
    LeadStatus,
)


class UpdateLeadPayload(BaseAutomationPayload):
    """
    Payload used by UpdateLeadHandler.
    """

    lead_id: int

    status: LeadStatus