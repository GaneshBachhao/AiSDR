from enum import StrEnum


class CompanySize(StrEnum):
    """
    Company size classification.
    """

    MICRO = "Micro"

    SMALL = "Small"

    MEDIUM = "Medium"

    LARGE = "Large"

    ENTERPRISE = "Enterprise"