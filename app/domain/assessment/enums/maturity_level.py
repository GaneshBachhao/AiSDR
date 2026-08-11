from enum import StrEnum


class MaturityLevel(StrEnum):
    """
    Represents the AI maturity level of an organization.
    """

    INITIAL = "Initial"

    DEVELOPING = "Developing"

    DEFINED = "Defined"

    MANAGED = "Managed"

    OPTIMIZED = "Optimized"