"""
Enterprise Intelligence Orchestrator

Coordinates all intelligence engines.
"""

from app.intelligence.common.schemas import (
    IntelligenceReport,
)

from app.intelligence.services.extraction_service import (
    ExtractionService,
)

from app.intelligence.services.scoring_service import (
    ScoringService,
)

from app.intelligence.services.reasoning_service import (
    ReasoningService,
)


class IntelligenceOrchestrator:
    """
    Central intelligence orchestrator.

    Executes:

    Extraction
        ↓
    Scoring
        ↓
    Reasoning
    """

    def __init__(self):

        self.extractor = ExtractionService()

        self.scorer = ScoringService()

        self.reasoner = ReasoningService()

    def analyze(
        self,
        text: str,
    ) -> IntelligenceReport:
        """
        Analyze business content.
        """

        evidence = self.extractor.extract(
            text,
        )

        scores = self.scorer.score(
            evidence,
        )

        report = IntelligenceReport(

            evidence=evidence,

            scores=scores,

        )

        report = self.reasoner.reason(
            report,
        )

        report.overall_score = self._calculate_overall_score(
            report,
        )

        report.summary = self._generate_summary(
            report,
        )

        report.recommendations = (
            self._collect_recommendations(
                report,
            )
        )

        return report

    def _calculate_overall_score(
        self,
        report: IntelligenceReport,
    ) -> float:

        if not report.scores:

            return 0.0

        total = sum(
            score.score
            for score in report.scores
        )

        return round(
            total / len(report.scores),
            2,
        )

    def _generate_summary(
        self,
        report: IntelligenceReport,
    ) -> str:

        if not report.insights:

            return (
                "No significant business insights detected."
            )

        return (
            f"{len(report.insights)} business "
            f"insight(s) generated."
        )

    def _collect_recommendations(
        self,
        report: IntelligenceReport,
    ) -> list[str]:

        recommendations = []

        for insight in report.insights:

            if (
                insight.recommendation
                not in recommendations
            ):

                recommendations.append(
                    insight.recommendation,
                )

        return recommendations