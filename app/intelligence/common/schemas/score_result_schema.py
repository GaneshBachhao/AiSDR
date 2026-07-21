"""
Score Result Schema

Represents the output of an enterprise scorer.
"""

from pydantic import BaseModel

from app.intelligence.common.schemas.evidence_schema import (
    Evidence,
)


class ScoreResult(BaseModel):
    """
    Explainable score.
    """

    name: str

    score: float

    confidence: float

    matched_evidence: list[Evidence] = []

    reasons: list[str] = []

    recommendations: list[str] = []