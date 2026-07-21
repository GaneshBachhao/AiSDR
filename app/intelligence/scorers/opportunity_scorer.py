"""
Opportunity Scorer
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


class OpportunityScorer(BaseScorer):

    SIGNALS = {
        "increase sales",
        "save time",
        "reduce cost",
        "automation",
    }

    def score(
        self,
        evidence: list[Evidence],
    ) -> ScoreResult:

        score = 30

        matched = []

        for item in evidence:

            if item.text.lower() in self.SIGNALS:

                score += 15
                matched.append(item)

        return ScoreResult(

            name="Business Opportunity",

            score=self.normalize(score),

            confidence=0.92,

            matched_evidence=matched,

            reasons=[
                "Business improvement opportunities detected."
            ],

            recommendations=[
                "Offer AI Consulting Engagement."
            ],
        )