"""
Close Conversation Handler
"""

from sqlalchemy.orm import Session

from app.automation.handlers.base_handler import (
    BaseAutomationHandler,
)

from app.automation.schemas.automation_action_schema import (
    AutomationAction,
)


class CloseConversationHandler(BaseAutomationHandler):
    """
    Closes a conversation.
    """

    def execute(
        self,
        db: Session,
        action: AutomationAction,
    ) -> None:

        #
        # TODO:
        # Integrate Conversation Service
        #

        return