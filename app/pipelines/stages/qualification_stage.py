"""
Qualification Pipeline Stage

Evaluates a CompanyProfile against the
Ideal Customer Profile (ICP).
"""

from app.core.logger import logger

from app.lead_intelligence.qualification.factories.icp_factory import (
    ICPFactory,
)

from app.lead_intelligence.qualification.services.qualification_service import (
    QualificationService,
)

from app.pipelines.context.pipeline_context import (
    PipelineContext,
)

from app.pipelines.stages.base_stage import (
    BasePipelineStage,
)


class QualificationStage(
    BasePipelineStage,
):
    """
    Qualifies an enriched company against
    the configured ICP.
    """

    @property
    def stage_name(self) -> str:
        return "Qualification"

    def __init__(
        self,
        qualification_service: QualificationService | None = None,
    ):

        self.qualification_service = (
            qualification_service
            if qualification_service
            else QualificationService()
        )

    def can_execute(
        self,
        context: PipelineContext,
    ) -> bool:

        return context.company_profile is not None

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:

        if context.company_profile is None:

            raise ValueError(
                "PipelineContext.company_profile is required."
            )

        logger.info(
            f"Qualifying Company : "
            f"{context.company_profile.company_name}"
        )

        icp = ICPFactory.from_request(
            context.request,
        )

        context.qualification = (
            self.qualification_service.qualify(
                company=context.company_profile,
                icp=icp,
            )
        )

        context.stage_results[
            self.stage_name
        ] = {

            "qualified": (
                context.qualification.qualified
            ),

            "score": (
                context.qualification.score
            ),

           "matched_rules": context.qualification.matched_rules,

            "failed_rules": (
                context.qualification.failed_rules
            ),
        }

        logger.info(
            f"Qualification Completed | "
            f"Qualified="
            f"{context.qualification.qualified} | "
            f"Score="
            f"{context.qualification.score}"
        )

        return context