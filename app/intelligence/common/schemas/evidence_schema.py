"""
Evidence Schema

Represents a single piece of evidence detected
during intelligence analysis.
"""

from pydantic import BaseModel
from pydantic import Field


class Evidence(BaseModel):
    """
    A single evidence item.
    """

    category: str = Field(
        description="Evidence category.",
    )

    source: str = Field(
        description="Origin of the evidence.",
    )

    text: str = Field(
        description="Raw extracted text.",
    )

    confidence: float = Field(
        ge=0,
        le=1,
        description="Confidence score.",
    )

    weight: float = Field(
        default=1.0,
        ge=0,
        description="Relative importance.",
    )