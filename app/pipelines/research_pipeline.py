from sqlalchemy.orm import Session

from app.core.logger import logger
from app.services.research_service import ResearchService


class ResearchPipeline:
    """
    Orchestrates the complete research workflow.
    """

    def __init__(self):
        self.research_service = ResearchService()

    def execute(
        self,
        db: Session,
        lead_id: int,
    ):

        logger.info("=" * 60)
        logger.info("Research Pipeline Started")

        result = self.research_service.research_lead(
            db=db,
            lead_id=lead_id,
        )

        logger.info("Research Pipeline Completed")
        logger.info("=" * 60)

        return result