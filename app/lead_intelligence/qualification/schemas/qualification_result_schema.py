"""
Qualification Result Schema

Represents the outcome of evaluating a
LeadCandidate against an Ideal Customer Profile.
"""

from pydantic import BaseModel, Field


class QualificationResult(BaseModel):
    """
    Result returned by the qualification engine.
    """

    qualified: bool = Field(
        ...,
        description="Whether the lead passed qualification",
    )

    score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Qualification score",
    )

    matched_rules: list[str] = Field(
        default_factory=list,
        description="Rules that positively matched",
    )

    failed_rules: list[str] = Field(
        default_factory=list,
        description="Rules that failed",
    )

    recommendations: list[str] = Field(
        default_factory=list,
        description="Suggested improvements or follow-up actions",
    )