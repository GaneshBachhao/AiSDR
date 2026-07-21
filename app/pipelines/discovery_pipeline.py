from sqlalchemy.orm import Session

from app.core.logger import logger

from app.discovery.schemas.discovery_schema import DiscoveryRequest
from app.discovery.services.discovery_service import DiscoveryService

from app.research.agents.research_agent import ResearchAgent


class DiscoveryPipeline:
    """
    Orchestrates the complete discovery workflow.
    """

    def __init__(self):

        self.discovery_service = DiscoveryService()
        self.research_agent = ResearchAgent()

    def execute(
        self,
        db: Session,
        request: DiscoveryRequest,
    ):

        logger.info("=" * 60)
        logger.info("Discovery Pipeline Started")

        discovery_result = self.discovery_service.discover(
            db=db,
            request=request,
        )

        research_completed = 0
        research_failed = 0

        for lead in discovery_result["created"]:

            try:

                self.research_agent.execute_async(
                    lead_id=lead.id,
                )

                research_completed += 1

                logger.info(
                    f"Research queued: {lead.company_name}"
                )

            except Exception as ex:

                research_failed += 1

                logger.exception(
                    f"Failed to queue research for "
                    f"{lead.company_name}: {str(ex)}"
                )

        logger.info(
            "Discovery completed. "
            f"Created={len(discovery_result['created'])}, "
            f"Skipped={len(discovery_result['skipped'])}, "
            f"ResearchQueued={research_completed}, "
            f"ResearchFailed={research_failed}"
        )

        logger.info("Discovery Pipeline Completed")
        logger.info("=" * 60)

        return {

            "created_count": len(
                discovery_result["created"]
            ),

            "created_ids": [
                lead.id
                for lead in discovery_result["created"]
            ],

            "created_companies": [
                lead.company_name
                for lead in discovery_result["created"]
            ],

            "skipped_count": len(
                discovery_result["skipped"]
            ),

            "skipped_companies": list(
                discovery_result["skipped"]
            ),

            "research_completed": research_completed,

            "research_failed": research_failed,
        }