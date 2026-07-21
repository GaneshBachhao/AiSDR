"""
Engagement Scorer
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


class EngagementScorer(BaseScorer):

    SIGNALS = {
        "meeting",
        "demo",
        "call",
        "interested",
        "schedule",
    }

    def score(
        self,
        evidence: list[Evidence],
    ) -> ScoreResult:

        score = 20

        matched = []

        for item in evidence:

            if item.text.lower() in self.SIGNALS:

                score += 20
                matched.append(item)

        return ScoreResult(

            name="Engagement",

            score=self.normalize(score),

            confidence=0.93,

            matched_evidence=matched,

            reasons=[
                "Strong engagement intent detected."
            ],

            recommendations=[
                "Prioritize immediate follow-up."
            ],
        )