"""
Qualification score value object.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class QualificationScore:
    """
    Represents the overall qualification score.

    Score range:
        0 - 100
    """

    value: float

    def __post_init__(
        self,
    ) -> None:
        """
        Validate score.
        """

        if self.value < 0 or self.value > 100:
            raise ValueError(
                "Qualification score must be between 0 and 100.",
            )

    @property
    def percentage(
        self,
    ) -> float:
        """
        Return the score as a percentage.
        """

        return self.value