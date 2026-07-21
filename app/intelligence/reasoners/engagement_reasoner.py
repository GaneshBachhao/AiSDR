"""
Engagement Reasoner
"""

from app.intelligence.common.schemas import (
    Insight,
    IntelligenceReport,
)

from app.intelligence.reasoners.base_reasoner import (
    BaseReasoner,
)


class EngagementReasoner(
    BaseReasoner,
):

    def reason(
        self,
        report: IntelligenceReport,
    ):

        insights = []

        for score in report.scores:

            if (
                score.name == "Engagement"
                and score.score >= 70
            ):

                insights.append(

                    Insight(

                        category="Sales",

                        title="High Engagement",

                        description=(
                            "Customer is actively engaged."
                        ),

                        confidence=score.confidence,

                        recommendation=(
                            "Sales should follow up immediately."
                        ),
                    )

                )

        return insights