"""
AI Readiness Reasoner
"""

from app.intelligence.common.schemas import (
    Insight,
    IntelligenceReport,
)

from app.intelligence.reasoners.base_reasoner import (
    BaseReasoner,
)


class AIReadinessReasoner(
    BaseReasoner,
):

    def reason(
        self,
        report: IntelligenceReport,
    ):

        insights = []

        for score in report.scores:

            if (
                score.name == "AI Readiness"
                and score.score >= 80
            ):

                insights.append(

                    Insight(

                        category="AI",

                        title="High AI Readiness",

                        description=(
                            "Organization appears ready "
                            "for AI adoption."
                        ),

                        confidence=score.confidence,

                        recommendation=(
                            "Offer AI Readiness Assessment."
                        ),
                    )

                )

        return insights