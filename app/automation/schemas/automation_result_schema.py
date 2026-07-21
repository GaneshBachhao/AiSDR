"""
Automation Result Schema
"""

from pydantic import BaseModel, Field

from app.automation.schemas.automation_action_schema import (
    AutomationAction,
)


class AutomationResult(BaseModel):
    """
    Result returned by the automation engine.
    """

    actions: list[AutomationAction] = Field(
        default_factory=list,
    )

    success: bool = True

    message: str = ""

    warnings: list[str] = Field(
        default_factory=list,
    )