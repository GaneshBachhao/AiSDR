from dataclasses import dataclass


@dataclass(frozen=True)
class BusinessBenefit:
    """
    Represents an expected business benefit.

    Business benefits describe the positive business outcomes
    expected from implementing a recommended AI solution.
    """

    title: str

    description: str

    measurable: bool = False

    def __post_init__(self) -> None:
        """
        Validate business invariants.
        """
        if not self.title.strip():
            raise ValueError("Business benefit title cannot be empty.")

        if not self.description.strip():
            raise ValueError("Business benefit description cannot be empty.")
