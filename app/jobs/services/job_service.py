import json

from datetime import datetime

from sqlalchemy.orm import Session

from app.common.utils.datetime_utils import utc_now, normalize_datetime
from app.jobs.enums.job_status import JobStatus
from app.jobs.enums.job_type import JobType
from app.jobs.models.job import Job
from app.jobs.repositories.job_repository import JobRepository
from app.jobs.schemas.job_schema import JobCreate, JobUpdate
from app.common.utils.id_generator import generate_correlation_id, generate_job_id


class JobService:

    def __init__(self):
        self.repository = JobRepository()

    def create_job(
        self,
        db: Session,
        job_type: JobType,
        input_payload: dict | None = None,
    ) -> Job:

        correlation_id = generate_correlation_id()

        job = JobCreate(
            job_id=generate_job_id(job_type),
            correlation_id=correlation_id,
            job_type=job_type,
            status=JobStatus.PENDING,
            input_payload=json.dumps(input_payload) if input_payload else None,
        )

        return self.repository.create(db, job)

    def start_job(
        self,
        db: Session,
        job: Job,
    ) -> Job:

        return self.repository.update(
            db,
            job,
            JobUpdate(
                status=JobStatus.RUNNING,
                started_at=utc_now(),
            ),
        )

    def complete_job(
        self,
        db: Session,
        job: Job,
        result_payload: dict | None = None,
    ) -> Job:

        completed_at = utc_now()

        duration = None

        started_at = normalize_datetime(job.started_at)

        if started_at:
            duration = (
                completed_at - started_at
            ).total_seconds()

        return self.repository.update(
            db,
            job,
            JobUpdate(
                status=JobStatus.COMPLETED,
                completed_at=completed_at,
                duration_seconds=duration,
                result_payload=json.dumps(result_payload)
                if result_payload
                else None,
            ),
        )

    def fail_job(
        self,
        db: Session,
        job: Job,
        error_message: str,
    ) -> Job:

        completed_at = utc_now()

        duration = None

        started_at = normalize_datetime(job.started_at)

        if started_at:
            duration = (
                completed_at - started_at
            ).total_seconds()

        return self.repository.update(
            db,
            job,
            JobUpdate(
                status=JobStatus.FAILED,
                completed_at=completed_at,
                duration_seconds=duration,
                error_message=error_message,
            ),
        )

    def get_job(
        self,
        db: Session,
        job_id: str,
    ) -> Job | None:

        return self.repository.get_by_job_id(
            db,
            job_id,
        )

    def list_jobs(
        self,
        db: Session,
    ) -> list[Job]:

        return self.repository.get_all(db)