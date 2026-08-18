from dataclasses import dataclass, field

from app.domain.assessment.value_objects.assessment_dimension import (
    AssessmentDimension,
)


@dataclass(frozen=True)
class AssessmentScore:
    """
    Represents the overall assessment score.

    The score is composed of multiple scored assessment
    dimensions and an overall weighted score.
    """

    overall_score: float = 0.0

    dimensions: tuple[AssessmentDimension, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:

        if not 0 <= self.overall_score <= 100:
            raise ValueError("Overall score must be between 0 and 100.")
