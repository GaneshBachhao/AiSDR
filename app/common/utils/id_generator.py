from datetime import datetime
import uuid

from app.jobs.enums.job_type import JobType


def generate_job_id(job_type: JobType) -> str:
    """
    Generate a unique, human-readable job ID.

    Example:
    DISCOVERY-20260710-143015-A7F3
    """

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    suffix = uuid.uuid4().hex[:4].upper()

    return f"{job_type.value}-{timestamp}-{suffix}"

def generate_correlation_id() -> str:
    """
    Generate a correlation ID for tracing.

    Example:
    CORR-8A12F0BC
    """

    return f"CORR-{uuid.uuid4().hex[:8].upper()}"