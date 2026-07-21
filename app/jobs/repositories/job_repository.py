from sqlalchemy.orm import Session

from app.jobs.models.job import Job
from app.jobs.schemas.job_schema import JobCreate, JobUpdate


class JobRepository:

    def create(
        self,
        db: Session,
        job: JobCreate
    ) -> Job:

        db_job = Job(
            **job.model_dump()
        )

        db.add(db_job)

        db.commit()

        db.refresh(db_job)

        return db_job

    def get_by_id(
        self,
        db: Session,
        job_id: int
    ) -> Job | None:

        return (
            db.query(Job)
            .filter(Job.id == job_id)
            .first()
        )

    def get_by_job_id(
        self,
        db: Session,
        job_id: str
    ) -> Job | None:

        return (
            db.query(Job)
            .filter(Job.job_id == job_id)
            .first()
        )

    def get_all(
        self,
        db: Session
    ) -> list[Job]:

        return (
            db.query(Job)
            .order_by(Job.created_at.desc())
            .all()
        )

    def get_running_jobs(
        self,
        db: Session
    ) -> list[Job]:

        from app.jobs.enums.job_status import JobStatus

        return (
            db.query(Job)
            .filter(Job.status == JobStatus.RUNNING)
            .all()
        )

    def update(
        self,
        db: Session,
        job: Job,
        updates: JobUpdate
    ) -> Job:

        update_data = updates.model_dump(
            exclude_unset=True,
            exclude_none=True
        )

        for key, value in update_data.items():
            setattr(job, key, value)

        db.commit()

        db.refresh(job)

        return job

    def delete(
        self,
        db: Session,
        job: Job
    ):

        db.delete(job)

        db.commit()