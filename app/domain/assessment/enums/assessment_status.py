from enum import StrEnum


class AssessmentStatus(StrEnum):
    """
    Represents the lifecycle of an assessment.
    """

    CREATED = "Created"

    IN_PROGRESS = "In Progress"

    UNDER_REVIEW = "Under Review"

    COMPLETED = "Completed"

    CANCELLED = "Cancelled"