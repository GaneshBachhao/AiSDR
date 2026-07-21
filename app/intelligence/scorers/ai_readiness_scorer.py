"""
AI Readiness Scorer
"""

from app.intelligence.common.schemas import (
    Evidence,
)

from app.intelligence.common.schemas.score_result_schema import (
    ScoreResult,
)

from app.intelligence.scorers.base_scorer import (
    BaseScorer,
)


class AIReadinessScorer(BaseScorer):

    POSITIVE = {
        "automation",
        "ai",
        "digital transformation",
        "workflow",
    }

    def score(
        self,
        evidence: list[Evidence],
    ) -> ScoreResult:

        score = 25

        matched = []

        for item in evidence:

            if item.text.lower() in self.POSITIVE:

                score += 20
                matched.append(item)

        return ScoreResult(

            name="AI Readiness",

            score=self.normalize(score),

            confidence=0.95,

            matched_evidence=matched,

            reasons=[
                "Automation and AI adoption signals detected."
            ],

            recommendations=[
                "Recommend AI Readiness Assessment."
            ],
        )