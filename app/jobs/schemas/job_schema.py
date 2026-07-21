from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.jobs.enums.job_status import JobStatus
from app.jobs.enums.job_type import JobType


class JobCreate(BaseModel):
    job_id: str
    correlation_id: str

    job_type: JobType

    status: JobStatus = JobStatus.PENDING

    input_payload: str | None = None


class JobUpdate(BaseModel):
    status: JobStatus | None = None

    started_at: datetime | None = None

    completed_at: datetime | None = None

    duration_seconds: float | None = None

    result_payload: str | None = None

    error_message: str | None = None


class JobResponse(BaseModel):

    id: int

    job_id: str

    correlation_id: str

    job_type: JobType

    status: JobStatus

    started_at: datetime | None

    completed_at: datetime | None

    duration_seconds: float | None

    error_message: str | None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )