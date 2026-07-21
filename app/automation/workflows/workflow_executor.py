"""
Workflow Executor

Executes automation actions using registered handlers.
"""

from sqlalchemy.orm import Session

from app.automation.handlers.automation_handler_factory import (
    AutomationHandlerFactory,
)

from app.automation.schemas.automation_result_schema import (
    AutomationResult,
)


class WorkflowExecutor:
    """
    Executes automation actions.
    """

    def execute(
        self,
        db: Session,
        result: AutomationResult,
    ) -> list[str]:
        """
        Execute all automation actions.

        Returns a list of successfully executed action names.
        """

        executed: list[str] = []

        for action in result.actions:

            handler = AutomationHandlerFactory.get_handler(
                action.action,
            )

            handler.execute(
                db=db,
                action=action,
            )

            executed.append(
                action.action.value,
            )

        return executed