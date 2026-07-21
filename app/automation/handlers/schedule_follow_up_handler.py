"""
Schedule Follow-up Handler
"""

from sqlalchemy.orm import Session

from app.automation.handlers.base_handler import (
    BaseAutomationHandler,
)

from app.automation.schemas.automation_action_schema import (
    AutomationAction,
)


class ScheduleFollowUpHandler(BaseAutomationHandler):
    """
    Schedules a follow-up.
    """

    def execute(
        self,
        db: Session,
        action: AutomationAction,
    ) -> None:

        #
        # TODO:
        # Integrate Scheduler Service
        #

        return