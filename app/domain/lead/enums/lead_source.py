from enum import StrEnum


class LeadSource(StrEnum):
    """
    Origin of a lead.
    """

    WEBSITE = "Website"

    REFERRAL = "Referral"

    LINKEDIN = "LinkedIn"

    EMAIL = "Email"

    PHONE = "Phone"

    EVENT = "Event"

    PARTNER = "Partner"

    OTHER = "Other"