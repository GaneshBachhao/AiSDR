"""
Signal Schema

Represents a business signal inferred
from one or more evidence items.
"""

from pydantic import BaseModel
from pydantic import Field

from app.intelligence.common.schemas.evidence_schema import (
    Evidence,
)


class Signal(BaseModel):
    """
    Business signal.
    """

    category: str = Field(
        description="Signal category.",
    )

    description: str = Field(
        description="Human readable description.",
    )

    importance: float = Field(
        ge=0,
        le=1,
    )

    evidence: list[Evidence] = Field(
        default_factory=list,
    )