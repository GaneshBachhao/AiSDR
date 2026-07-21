"""
Risk Scorer
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


class RiskScorer(BaseScorer):

    NEGATIVE = {
        "budget",
        "expensive",
        "delay",
        "legacy",
    }

    def score(
        self,
        evidence: list[Evidence],
    ) -> ScoreResult:

        score = 10

        matched = []

        for item in evidence:

            if item.text.lower() in self.NEGATIVE:

                score += 20
                matched.append(item)

        return ScoreResult(

            name="Risk",

            score=self.normalize(score),

            confidence=0.90,

            matched_evidence=matched,

            reasons=[
                "Potential implementation risks identified."
            ],

            recommendations=[
                "Perform detailed discovery before proposal."
            ],
        )