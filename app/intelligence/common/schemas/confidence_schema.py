"""
Confidence Schema

Stores explainable confidence
information.
"""

from pydantic import BaseModel
from pydantic import Field

from app.intelligence.common.schemas.signal_schema import (
    Signal,
)


class Confidence(BaseModel):
    """
    Confidence calculation.
    """

    overall: float = Field(
        ge=0,
        le=1,
    )

    signals: list[Signal] = Field(
        default_factory=list,
    )

    positive_factors: list[str] = Field(
        default_factory=list,
    )

    negative_factors: list[str] = Field(
        default_factory=list,
    )

    explanation: str = Field(
        default="",
    )