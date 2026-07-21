"""
Base Automation Handler

Provides common functionality for all automation handlers.
"""

from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

from pydantic import BaseModel

from app.automation.schemas.automation_action_schema import (
    AutomationAction,
)

PayloadT = TypeVar(
    "PayloadT",
    bound=BaseModel,
)


class BaseAutomationHandler(
    ABC,
    Generic[PayloadT],
):
    """
    Base class for all automation handlers.
    """

    payload_model: type[PayloadT]

    # =====================================================
    # Payload
    # =====================================================

    def parse_payload(
        self,
        action: AutomationAction,
    ) -> PayloadT:
        """
        Validate and deserialize the payload.
        """

        return self.payload_model.model_validate(
            action.payload,
        )

    # =====================================================
    # Lifecycle Hooks
    # =====================================================

    def before_execute(
        self,
        action: AutomationAction,
    ) -> None:
        """
        Hook executed before the handler.

        Override if needed.
        """

        pass

    def after_execute(
        self,
        action: AutomationAction,
    ) -> None:
        """
        Hook executed after the handler.

        Override if needed.
        """

        pass

    def on_error(
        self,
        action: AutomationAction,
        exception: Exception,
    ) -> None:
        """
        Hook executed on failure.

        Default behaviour is to re-raise.
        """

        raise exception

    # =====================================================
    # Execution Template
    # =====================================================

    def handle(
        self,
        db,
        action: AutomationAction,
    ) -> None:
        """
        Executes the handler lifecycle.

        Do not override.
        """

        try:

            self.before_execute(
                action,
            )

            self.execute(
                db,
                action,
            )

            self.after_execute(
                action,
            )

        except Exception as ex:

            self.on_error(
                action,
                ex,
            )

    # =====================================================
    # Business Execution
    # =====================================================

    @abstractmethod
    def execute(
        self,
        db,
        action: AutomationAction,
    ) -> None:
        """
        Execute the automation action.
        """