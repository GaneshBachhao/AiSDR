"""
Opportunity Reasoner
"""

from app.intelligence.common.schemas import (
    Insight,
    IntelligenceReport,
)

from app.intelligence.reasoners.base_reasoner import (
    BaseReasoner,
)


class OpportunityReasoner(
    BaseReasoner,
):

    def reason(
        self,
        report: IntelligenceReport,
    ):

        insights = []

        for score in report.scores:

            if (
                score.name == "Business Opportunity"
                and score.score >= 75
            ):

                insights.append(

                    Insight(

                        category="Opportunity",

                        title="Strong Consulting Opportunity",

                        description=(
                            "High-value opportunity detected."
                        ),

                        confidence=score.confidence,

                        recommendation=(
                            "Recommend consulting engagement."
                        ),
                    )

                )

        return insights