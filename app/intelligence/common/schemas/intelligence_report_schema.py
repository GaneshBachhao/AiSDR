"""
Enterprise Intelligence Report

Single intelligence object shared across all
AI BDOS intelligence engines.
"""

from pydantic import BaseModel
from pydantic import Field

from app.intelligence.common.schemas.evidence_schema import Evidence
from app.intelligence.common.schemas.insight_schema import Insight
from app.intelligence.common.schemas.score_result_schema import ScoreResult


class IntelligenceReport(BaseModel):
    """
    Unified intelligence report.
    """

    evidence: list[Evidence] = Field(default_factory=list)

    scores: list[ScoreResult] = Field(default_factory=list)

    insights: list[Insight] = Field(default_factory=list)

    recommendations: list[str] = Field(default_factory=list)

    metadata: dict[str, str] = Field(default_factory=dict)

    summary: str | None = None

    overall_score: float = 0.0