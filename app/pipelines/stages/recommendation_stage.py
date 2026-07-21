"""
Recommendation Stage

Generates AI service recommendations
from the enriched company profile.
"""

from app.knowledge.research_enrichment import (
    ResearchEnrichment,
)

from app.pipelines.context.pipeline_context import (
    PipelineContext,
)

from app.pipelines.stages.base_stage import (
    BasePipelineStage,
)

from app.recommendation.services.recommendation_service import (
    RecommendationService,
)


class RecommendationStage(BasePipelineStage):
    """
    Generates AI recommendations.
    """

    stage_name = "Recommendation"

    def __init__(self):

        self.enrichment = ResearchEnrichment()

        self.service = RecommendationService()

    # ======================================================
    # Can Execute
    # ======================================================

    def can_execute(
        self,
        context: PipelineContext,
    ) -> bool:

        return context.company_profile is not None

    # ======================================================
    # Execute
    # ======================================================

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:

        enriched = self.enrichment.enrich(

            company_profile=context.company_profile,

        )

        recommendations = self.service.generate(
            enriched,
        )

        context.recommendations = (
            recommendations
        )

        context.stage_results[
            self.stage_name
        ] = {

            "recommendations": len(
                recommendations.recommendations
            ),

            "sector": recommendations.matched_sector,
        }

        return context