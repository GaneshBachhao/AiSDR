"""
Company Intelligence Pipeline Stage

Enriches a LeadCandidate into a CompanyProfile
using the configured Company Intelligence provider.
"""

from app.core.logger import logger

from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)

from app.company_intelligence.services.company_intelligence_service import (
    CompanyIntelligenceService,
)

from app.pipelines.context.pipeline_context import (
    PipelineContext,
)

from app.pipelines.stages.base_stage import (
    BasePipelineStage,
)


class CompanyIntelligenceStage(
    BasePipelineStage,
):
    """
    Enriches a LeadCandidate into a CompanyProfile.

    If enrichment fails, a fallback CompanyProfile is
    created so downstream pipeline stages can continue.
    """

    @property
    def stage_name(self) -> str:
        return "Company Intelligence"

    def __init__(
        self,
        service: CompanyIntelligenceService | None = None,
    ):
        self.service = (
            service
            if service
            else CompanyIntelligenceService()
        )

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:

        if context.candidate is None:
            raise ValueError(
                "PipelineContext.candidate is required."
            )

        logger.info(
            f"Enriching company: "
            f"{context.candidate.company_name}"
        )

        try:

            profile = self.service.enrich(
                context.candidate,
            )

            context.company_profile = profile

            context.stage_results[
                self.stage_name
            ] = {
                "success": True,
                "fallback": False,
                "company": profile.company_name,
            }

            logger.info(
                f"Company enrichment completed: "
                f"{profile.company_name}"
            )

        except Exception as ex:

            logger.exception(
                f"Company enrichment failed for "
                f"{context.candidate.company_name}"
            )

            context.warnings.append(
                f"Company Intelligence fallback used: {str(ex)}"
            )

            context.company_profile = CompanyProfile(
                company_name=context.candidate.company_name,
                website=(
                    str(context.candidate.website)
                    if context.candidate.website
                    else None
                ),
                industry=context.candidate.industry,
                country=context.candidate.country,
                state=context.candidate.state,
                city=context.candidate.city,
                employee_count=context.candidate.employee_count,
            )

            context.stage_results[
                self.stage_name
            ] = {
                "success": True,
                "fallback": True,
                "company": context.company_profile.company_name,
            }

        return context