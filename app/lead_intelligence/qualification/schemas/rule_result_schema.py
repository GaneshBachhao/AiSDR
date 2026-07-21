"""
Rule Result Schema

Represents the outcome of evaluating
a single qualification rule.
"""

from pydantic import BaseModel, Field


class RuleResult(BaseModel):
    """
    Result returned by a qualification rule.
    """

    passed: bool = Field(
        ...,
        description="Whether the rule passed",
    )

    score: float = Field(
        default=0,
        ge=0,
        le=100,
    )

    rule_name: str = Field(
        ...,
        description="Rule name",
    )

    message: str = Field(
        ...,
        description="Rule evaluation message",
    )

    recommendation: str | None = Field(
        default=None,
        description="Suggested action",
    )