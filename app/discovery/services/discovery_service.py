"""
Discovery Service

Responsible for discovering lead candidates and
executing the lead processing pipeline.
"""

from app.core.logger import logger

from app.discovery.providers.provider_factory import (
    DiscoveryProviderFactory,
)

from app.discovery.schemas.discovery_schema import (
    DiscoveryRequest,
)

from app.pipelines.context.pipeline_context import (
    PipelineContext,
)

from app.pipelines.orchestrator import (
    PipelineOrchestrator,
)

from app.pipelines.stages.company_intelligence_stage import (
    CompanyIntelligenceStage,
)

from app.pipelines.stages.qualification_stage import (
    QualificationStage,
)

from app.pipelines.stages.lead_creation_stage import (
    LeadCreationStage,
)


class DiscoveryService:
    """
    Discovers companies and processes them
    through the discovery pipeline.
    """

    def __init__(self):

        self.provider = (
            DiscoveryProviderFactory.get_provider()
        )

        self.orchestrator = PipelineOrchestrator(
            stages=[
                CompanyIntelligenceStage(),
                QualificationStage(),
                LeadCreationStage(),
            ]
        )

    def discover(
        self,
        db,
        request: DiscoveryRequest,
    ):

        logger.info("=" * 80)
        logger.info("Starting Lead Discovery")
        logger.info("=" * 80)

        candidates = self.provider.discover(
            industry=request.industry,
            location=request.location,
            max_results=request.max_results,
        )

        logger.info(
            f"Discovered {len(candidates)} companies."
        )

        created: list = []
        skipped: list = []

        for candidate in candidates:

            logger.info(
                f"Processing Candidate : "
                f"{candidate.company_name}"
            )

            context = PipelineContext(
                db=db,
                request=request,
                candidate=candidate,
            )

            context = self.orchestrator.execute(
                context
            )

            if context.lead is not None:

                created.append(
                    context.lead
                )

                logger.info(
                    f"[CREATED] "
                    f"{context.lead.company_name}"
                )

            else:

                skipped.append(
                    {
                        "company": candidate.company_name,
                        "status": context.status,
                        "errors": context.errors,
                        "warnings": context.warnings,
                        "stage_results": context.stage_results,
                    }
                )

                logger.info(
                    f"[SKIPPED] "
                    f"{candidate.company_name}"
                )

        logger.info("=" * 80)
        logger.info(
            f"Discovery Completed | "
            f"Created={len(created)} | "
            f"Skipped={len(skipped)}"
        )
        logger.info("=" * 80)

        return {
            "created": created,
            "skipped": skipped,
        }