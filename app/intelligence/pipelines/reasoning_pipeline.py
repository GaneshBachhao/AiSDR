"""
Reasoning Pipeline
"""

from app.intelligence.common.schemas import (
    IntelligenceReport,
)

from app.intelligence.registry.reasoner_registry import (
    ReasonerRegistry,
)


class ReasoningPipeline:
    """
    Executes enterprise reasoners.
    """

    def __init__(self):

        self.reasoners = (
            ReasonerRegistry.get_reasoners()
        )

    def run(
        self,
        report: IntelligenceReport,
    ) -> IntelligenceReport:

        insights = []

        for reasoner in self.reasoners:

            insights.extend(

                reasoner.reason(

                    report,

                )

            )

        report.insights.extend(

            insights,

        )

        return report