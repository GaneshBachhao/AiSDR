from enum import StrEnum


class SuppressionReason(StrEnum):
    """
    Why an email address was added to the do-not-contact list.
    """

    MANUAL = "Manual"

    BOUNCE = "Bounce"

    COMPLAINT = "Complaint"
