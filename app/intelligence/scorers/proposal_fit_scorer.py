"""
Proposal Fit Scorer
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


class ProposalFitScorer(BaseScorer):

    SIGNALS = {
        "automation",
        "workflow",
        "approval",
        "crm",
    }

    def score(
        self,
        evidence: list[Evidence],
    ) -> ScoreResult:

        score = 40

        matched = []

        for item in evidence:

            if item.text.lower() in self.SIGNALS:

                score += 15
                matched.append(item)

        return ScoreResult(

            name="Proposal Fit",

            score=self.normalize(score),

            confidence=0.94,

            matched_evidence=matched,

            reasons=[
                "Solution aligns well with customer needs."
            ],

            recommendations=[
                "Generate customized proposal."
            ],
        )