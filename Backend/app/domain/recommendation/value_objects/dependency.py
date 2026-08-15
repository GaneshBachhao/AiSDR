from dataclasses import dataclass


@dataclass(frozen=True)
class Dependency:
    """
    Represents a prerequisite for implementing
    a recommended solution.
    """

    name: str

    description: str | None = None

    def __post_init__(self) -> None:
        """
        Validate business invariants.
        """
        if not self.name.strip():
            raise ValueError(
                "Dependency name cannot be empty."
            )

        if (
            self.description is not None
            and not self.description.strip()
        ):
            raise ValueError(
                "Description cannot be empty."
            )