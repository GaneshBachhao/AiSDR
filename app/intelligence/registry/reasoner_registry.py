"""
Reasoner Registry
"""

from app.intelligence.reasoners import (
    AIReadinessReasoner,
    OpportunityReasoner,
    EngagementReasoner,
    ProposalReasoner,
    RiskReasoner,
)


class ReasonerRegistry:
    """
    Registry of enterprise reasoners.
    """

    @staticmethod
    def get_reasoners():

        return [

            AIReadinessReasoner(),

            OpportunityReasoner(),

            EngagementReasoner(),

            ProposalReasoner(),

            RiskReasoner(),

        ]