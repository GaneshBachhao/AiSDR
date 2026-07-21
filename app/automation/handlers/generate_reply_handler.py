"""
Generate Reply Handler
"""

from sqlalchemy.orm import Session

from app.automation.handlers.base_handler import (
    BaseAutomationHandler,
)

from app.automation.schemas.automation_action_schema import (
    AutomationAction,
)


class GenerateReplyHandler(BaseAutomationHandler):
    """
    Generates an AI reply.
    """

    def execute(
        self,
        db: Session,
        action: AutomationAction,
    ) -> None:

        #
        # TODO:
        # Integrate Reply Generation Service
        #

        return