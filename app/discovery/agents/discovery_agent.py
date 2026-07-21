
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.core.logger import logger
from app.discovery.schemas.discovery_schema import DiscoveryRequest
from app.pipelines.discovery_pipeline import DiscoveryPipeline

from app.jobs.services.job_service import JobService
from app.jobs.enums.job_type import JobType
from app.jobs.context.job_context import JobContext
from app.execution.job_execution import JobExecution

class DiscoveryAgent:
    """
    Orchestrates the complete lead discovery workflow.
    """

    def __init__(self):
        self.discovery_pipeline = DiscoveryPipeline()
        self.job_service = JobService()

    def execute(
        self,
        db: Session,
        request: DiscoveryRequest,
    ):
        """
        Execute discovery synchronously.
        """

        logger.info("=" * 60)
        logger.info("Discovery Agent Started")

        # Step 1 - Create Job
        job = self.job_service.create_job(
            db=db,
            job_type=JobType.DISCOVERY,
            input_payload=request.model_dump(),
        )

        logger.info(
            f"Created Job: {job.job_id}"
        )

        # Step 2 - Create Execution Context
        context = JobContext(job)

        # Step 3 - Execute inside the framework
        with JobExecution(
            db=db,
            context=context,
            service=self.job_service,
        ) as execution:

            result = self.discovery_pipeline.execute(
                db=db,
                request=request,
            )

            execution.result_payload = result

        logger.info("Discovery Agent Completed")
        logger.info("=" * 60)

        return result

    def execute_async(
        self,
        request: DiscoveryRequest,
    ):
        """
        Execute discovery in a background task using
        its own database session.
        """

        logger.info("=" * 60)
        logger.info("Background Discovery Started")

        db = SessionLocal()

        try:

            self.execute(
                db=db,
                request=request
            )

        except Exception as ex:

            logger.exception(
                f"Background Discovery Failed: {str(ex)}"
            )

        finally:

            db.close()

            logger.info("Database session closed.")

        logger.info("Background Discovery Finished")
        logger.info("=" * 60)