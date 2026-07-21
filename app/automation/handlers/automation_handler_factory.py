"""
Automation Handler Factory
"""

from app.automation.enums.action_type import (
    ActionType,
)

from app.automation.handlers.base_handler import (
    BaseAutomationHandler,
)

from app.automation.handlers.handler_registry import (
    HANDLER_REGISTRY,
)


class AutomationHandlerFactory:
    """
    Factory responsible for creating automation handlers.
    """

    @classmethod
    def get_handler(
        cls,
        action: ActionType,
    ) -> BaseAutomationHandler:
        """
        Return a handler instance for the given action.
        """

        handler_class = HANDLER_REGISTRY.get(
            action,
        )

        if handler_class is None:
            raise ValueError(
                f"No handler registered for action '{action}'."
            )

        return handler_class()