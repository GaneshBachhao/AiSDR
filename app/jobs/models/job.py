from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Text,
    Enum,
)

from sqlalchemy.sql import func

from app.database.database import Base

from app.jobs.enums.job_status import JobStatus
from app.jobs.enums.job_type import JobType


class Job(Base):

    __tablename__ = "jobs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    job_id = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    job_type = Column(
        Enum(JobType),
        nullable=False
    )

    status = Column(
        Enum(JobStatus),
        nullable=False,
        default=JobStatus.PENDING
    )

    correlation_id = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    started_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    duration_seconds = Column(
        Float,
        nullable=True
    )

    input_payload = Column(
        Text,
        nullable=True
    )

    result_payload = Column(
        Text,
        nullable=True
    )

    error_message = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now()
    )