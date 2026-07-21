"""
Proposal Reasoner
"""

from app.intelligence.common.schemas import (
    Insight,
    IntelligenceReport,
)

from app.intelligence.reasoners.base_reasoner import (
    BaseReasoner,
)


class ProposalReasoner(
    BaseReasoner,
):

    def reason(
        self,
        report: IntelligenceReport,
    ):

        insights = []

        for score in report.scores:

            if (
                score.name == "Proposal Fit"
                and score.score >= 80
            ):

                insights.append(

                    Insight(

                        category="Proposal",

                        title="Proposal Recommended",

                        description=(
                            "Customer aligns well "
                            "with consulting services."
                        ),

                        confidence=score.confidence,

                        recommendation=(
                            "Generate customized proposal."
                        ),
                    )

                )

        return insights