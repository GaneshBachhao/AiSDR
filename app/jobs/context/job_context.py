from dataclasses import dataclass

from app.jobs.enums.job_status import JobStatus
from app.jobs.enums.job_type import JobType
from app.jobs.models.job import Job


@dataclass(slots=True)
class JobContext:
    """
    Shared execution context for background jobs.
    """

    job: Job

    @property
    def job_id(self) -> str:
        return self.job.job_id

    @property
    def correlation_id(self) -> str:
        return self.job.correlation_id

    @property
    def status(self) -> JobStatus:
        return self.job.status

    @property
    def job_type(self) -> JobType:
        return self.job.job_type