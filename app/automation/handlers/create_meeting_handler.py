"""
Create Meeting Handler
"""

from sqlalchemy.orm import Session

from app.automation.handlers.base_handler import (
    BaseAutomationHandler,
)

from app.automation.schemas.automation_action_schema import (
    AutomationAction,
)


class CreateMeetingHandler(BaseAutomationHandler):
    """
    Creates a meeting.
    """

    def execute(
        self,
        db: Session,
        action: AutomationAction,
    ) -> None:

        #
        # TODO:
        # Integrate Calendar / Meeting Service
        #

        return