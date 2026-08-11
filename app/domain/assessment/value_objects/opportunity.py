from dataclasses import dataclass


@dataclass(frozen=True)
class Opportunity:
    """
    Represents an improvement opportunity identified
    during assessment.
    """

    title: str

    description: str

    business_impact: str

    implementation_effort: str

    estimated_roi: str | None = None

    def __post_init__(self) -> None:

        if not self.title.strip():
            raise ValueError(
                "Opportunity title cannot be empty."
            )

        if not self.description.strip():
            raise ValueError(
                "Opportunity description cannot be empty."
            )

        if not self.business_impact.strip():
            raise ValueError(
                "Business impact cannot be empty."
            )

        if not self.implementation_effort.strip():
            raise ValueError(
                "Implementation effort cannot be empty."
            )