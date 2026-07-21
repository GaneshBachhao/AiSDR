from pydantic import BaseModel, Field


class Reasoning(BaseModel):
    """
    Explains why AI produced a recommendation.
    """

    confidence: float = Field(
        ge=0,
        le=1,
    )

    signals: list[str] = Field(
        default_factory=list,
    )

    positive_indicators: list[str] = Field(
        default_factory=list,
    )

    negative_indicators: list[str] = Field(
        default_factory=list,
    )

    assumptions: list[str] = Field(
        default_factory=list,
    )

    risks: list[str] = Field(
        default_factory=list,
    )

    explanation: str = ""