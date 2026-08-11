from dataclasses import dataclass


@dataclass(frozen=True)
class AssessmentDimension:
    """
    Represents the score of a single assessment dimension.
    """

    name: str

    score: float

    weight: float

    remarks: str | None = None

    def __post_init__(self) -> None:

        if not self.name.strip():
            raise ValueError(
                "Dimension name cannot be empty."
            )

        if not 0 <= self.score <= 100:
            raise ValueError(
                "Score must be between 0 and 100."
            )

        if not 0 < self.weight <= 100:
            raise ValueError(
                "Weight must be greater than 0 and at most 100."
            )