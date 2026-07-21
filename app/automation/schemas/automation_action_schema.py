"""
Automation Action Schema
"""

from pydantic import BaseModel
from pydantic import Field

from app.automation.enums.action_type import (
    ActionType,
)

from app.automation.enums.automation_priority import (
    AutomationPriority,
)


class AutomationAction(BaseModel):
    """
    Represents a single automation command.
    """

    action: ActionType

    description: str

    priority: AutomationPriority = (
        AutomationPriority.MEDIUM
    )

    payload: dict[str, object] = Field(
        default_factory=dict,
    )