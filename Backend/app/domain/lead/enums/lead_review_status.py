from enum import StrEnum


class LeadReviewStatus(StrEnum):
    """
    Represents the human-in-the-loop review gate a Lead passes through
    before any outreach can be sent to it -- orthogonal to LeadStatus
    (the CRM lifecycle: New/Contacted/Qualified/...). A Qualified lead can
    still be NOT_SUBMITTED for review; the two axes are independent.

    Deliberately stops at APPROVED/REJECTED -- no SENT value exists yet,
    since no send/outreach mechanism exists anywhere in this codebase
    (EPIC-09, not yet built). Adding it now would be guessing its shape.
    """

    NOT_SUBMITTED = "Not Submitted"

    PENDING_REVIEW = "Pending Review"

    APPROVED = "Approved"

    REJECTED = "Rejected"
