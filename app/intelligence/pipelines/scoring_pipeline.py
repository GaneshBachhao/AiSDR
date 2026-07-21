"""
Scoring Pipeline
"""

from app.intelligence.common.schemas import (

    Evidence,

)

from app.intelligence.common.schemas.score_result_schema import (

    ScoreResult,

)

from app.intelligence.registry.scorer_registry import (

    ScorerRegistry,

)


class ScoringPipeline:
    """
    Executes every scorer.
    """

    def __init__(self):

        self.scorers = ScorerRegistry.get_scorers()

    def score(

        self,

        evidence: list[Evidence],

    ) -> list[ScoreResult]:

        results = []

        for scorer in self.scorers:

            results.append(

                scorer.score(

                    evidence,

                )

            )

        return results