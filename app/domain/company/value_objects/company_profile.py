from dataclasses import dataclass


@dataclass(frozen=True)
class CompanyProfile:
    """
    Business profile information.
    """

    industry: str

    size: str

    location: str | None = None