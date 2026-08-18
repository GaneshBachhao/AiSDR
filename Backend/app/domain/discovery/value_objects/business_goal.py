from dataclasses import dataclass


@dataclass(frozen=True)
class BusinessGoal:
    """
    Represents a business objective captured during discovery.

    A business goal describes what the organization wants
    to achieve and its importance level.
    """

    title: str

    description: str

    priority: int

    def __post_init__(self) -> None:

        if not self.title.strip():
            raise ValueError("Business goal title cannot be empty.")

        if not self.description.strip():
            raise ValueError("Business goal description cannot be empty.")

        if not 1 <= self.priority <= 5:
            raise ValueError("Priority must be between 1 and 5.")
