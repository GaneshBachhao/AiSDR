from enum import StrEnum


class RecommendationStatus(StrEnum):
    """
    Represents the lifecycle of a recommendation.
    """

    DRAFT = "Draft"

    UNDER_REVIEW = "Under Review"

    APPROVED = "Approved"

    REJECTED = "Rejected"

    ARCHIVED = "Archived"