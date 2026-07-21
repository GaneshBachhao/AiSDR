"""
Risk Reasoner
"""

from app.intelligence.common.schemas import (
    Insight,
    IntelligenceReport,
)

from app.intelligence.reasoners.base_reasoner import (
    BaseReasoner,
)


class RiskReasoner(
    BaseReasoner,
):

    def reason(
        self,
        report: IntelligenceReport,
    ):

        insights = []

        for score in report.scores:

            if (
                score.name == "Risk"
                and score.score >= 60
            ):

                insights.append(

                    Insight(

                        category="Risk",

                        title="Potential Risk",

                        description=(
                            "Business risks detected."
                        ),

                        confidence=score.confidence,

                        recommendation=(
                            "Conduct discovery before proposal."
                        ),
                    )

                )

        return insights