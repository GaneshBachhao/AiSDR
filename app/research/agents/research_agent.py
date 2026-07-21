
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.core.logger import logger

from app.jobs.context.job_context import JobContext
from app.jobs.enums.job_type import JobType
from app.jobs.services.job_service import JobService

from app.execution.job_execution import JobExecution

from app.pipelines.research_pipeline import ResearchPipeline


class ResearchAgent:
    """
    Orchestrates the complete research workflow.
    """

    def __init__(self):
        self.pipeline = ResearchPipeline()
        self.job_service = JobService()

    def execute(
        self,
        db: Session,
        lead_id: int,
    ):
        """
        Execute research synchronously.
        """

        logger.info("=" * 60)
        logger.info("Research Agent Started")

        job = self.job_service.create_job(
            db=db,
            job_type=JobType.RESEARCH,
            input_payload={
                "lead_id": lead_id
            },
        )

        context = JobContext(job)

        with JobExecution(
            db=db,
            context=context,
            service=self.job_service,
        ) as execution:

            result = self.pipeline.execute(
                db=db,
                lead_id=lead_id,
            )

            execution.result_payload = {
                "lead_id": lead_id,
                "research_id": result.id,
            }

        logger.info("Research Agent Completed")
        logger.info("=" * 60)

        return result
    



    def execute_async(
        self,
        lead_id: int,
    ):
        """
        Execute research in a background task using
        its own database session.
        """

        logger.info("=" * 60)
        logger.info("Background Research Started")

        db = SessionLocal()

        try:

            self.execute(
                db=db,
                lead_id=lead_id,
            )

        except Exception as ex:

            logger.exception(
                f"Background Research Failed: {str(ex)}"
            )

        finally:

            db.close()

            logger.info("Database session closed.")

        logger.info("Background Research Finished")
        logger.info("=" * 60)