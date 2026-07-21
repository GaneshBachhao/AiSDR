"""
Update Lead Handler

Updates the status of a lead using the LeadService.
"""

from sqlalchemy.orm import Session

from app.automation.handlers.base_handler import (
    BaseAutomationHandler,
)

from app.automation.payloads.update_lead_payload import (
    UpdateLeadPayload,
)

from app.automation.schemas.automation_action_schema import (
    AutomationAction,
)

from app.leads.enums.lead_status import (
    LeadStatus,
)

from app.services.lead_service import (
    LeadService,
)


class UpdateLeadHandler(
    BaseAutomationHandler[UpdateLeadPayload]
):
    """
    Handles lead status update automation.
    """

    payload_model = UpdateLeadPayload

    def __init__(
        self,
        lead_service: LeadService | None = None,
    ):
        self.service = lead_service or LeadService()

    def execute(
        self,
        db: Session,
        action: AutomationAction,
    ) -> None:

        payload = self.parse_payload(
            action,
        )

        status_handlers = {

            LeadStatus.QUALIFIED:
                self.service.qualify,

            LeadStatus.CONTACTED:
                self.service.mark_contacted,

            LeadStatus.MEETING_SCHEDULED:
                self.service.schedule_meeting,

            LeadStatus.PROPOSAL_SENT:
                self.service.mark_proposal_sent,

            LeadStatus.NEGOTIATION:
                self.service.mark_negotiation,

            LeadStatus.WON:
                self.service.mark_won,

            LeadStatus.LOST:
                self.service.mark_lost,

        }

        handler = status_handlers.get(
            payload.status,
        )

        if handler is None:

            raise ValueError(
                f"Unsupported lead status: {payload.status}"
            )

        handler(
            db,
            payload.lead_id,
        )