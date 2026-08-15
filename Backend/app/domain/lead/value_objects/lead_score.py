from dataclasses import dataclass


@dataclass(frozen=True)
class LeadScore:
    """
    Represents a lead qualification score.

    Valid range: 0-100
    """

    value: int = 0

    def __post_init__(self) -> None:
        if not 0 <= self.value <= 100:
            raise ValueError(
                "Lead score must be between 0 and 100."
            )

    @property
    def is_hot(self) -> bool:
        return self.value >= 80

    @property
    def is_warm(self) -> bool:
        return 50 <= self.value < 80

    @property
    def is_cold(self) -> bool:
        return self.value < 50