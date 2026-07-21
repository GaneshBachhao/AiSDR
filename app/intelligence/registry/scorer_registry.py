"""
Scorer Registry
"""

from app.intelligence.scorers import (

    AIReadinessScorer,

    OpportunityScorer,

    EngagementScorer,

    ProposalFitScorer,

    RiskScorer,

)


class ScorerRegistry:
    """
    Registry for all enterprise scorers.
    """

    @staticmethod
    def get_scorers():

        return [

            AIReadinessScorer(),

            OpportunityScorer(),

            EngagementScorer(),

            ProposalFitScorer(),

            RiskScorer(),

        ]