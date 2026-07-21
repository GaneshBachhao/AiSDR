from sqlalchemy.orm import Session

from app.jobs.context.job_context import JobContext
from app.jobs.services.job_service import JobService

from app.core.logger import logger

class JobExecution:
    """
    Context manager responsible for managing
    the lifecycle of a background job.
    """

    def __init__(
        self,
        db: Session,
        context: JobContext,
        service: JobService,
    ):

        self.db = db

        self.context = context

        self.service = service

        self.result_payload = None


    def __enter__(self):
        """
        Called automatically when entering the
        'with JobExecution(...)' block.
        """

        logger.info("=" * 60)
        logger.info(f"[{self.context.job_id}] Starting execution")

        self.context.job = self.service.start_job(
            self.db,
            self.context.job
        )

        logger.info(
            f"[{self.context.job_id}] Status: {self.context.status}"
        )

        return self
    

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        """
        Called automatically when leaving the
        'with JobExecution(...)' block.
        """

        if exc_type is None:

            self.context.job = self.service.complete_job(
                self.db,
                self.context.job,
                self.result_payload,
            )

            logger.info(
                f"[{self.context.job_id}] Execution completed successfully."
            )

        else:

            self.context.job = self.service.fail_job(
                self.db,
                self.context.job,
                str(exc_value),
            )

            logger.exception(
                f"[{self.context.job_id}] Execution failed: {exc_value}"
            )

        logger.info("=" * 60)

        # Never suppress exceptions.
        return False