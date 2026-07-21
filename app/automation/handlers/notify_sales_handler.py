"""
Notify Sales Handler
"""

from sqlalchemy.orm import Session

from app.automation.handlers.base_handler import (
    BaseAutomationHandler,
)

from app.automation.schemas.automation_action_schema import (
    AutomationAction,
)


class NotifySalesHandler(BaseAutomationHandler):
    """
    Sends notification to sales.
    """

    def execute(
        self,
        db: Session,
        action: AutomationAction,
    ) -> None:

        #
        # TODO:
        # Integrate Notification Service
        #

        return