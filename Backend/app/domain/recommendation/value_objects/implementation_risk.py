from dataclasses import dataclass


@dataclass(frozen=True)
class ImplementationRisk:
    """
    Represents a risk associated with implementing
    a proposed AI solution.
    """

    title: str

    description: str

    mitigation: str | None = None

    def __post_init__(self) -> None:
        """
        Validate business invariants.
        """
        if not self.title.strip():
            raise ValueError("Risk title cannot be empty.")

        if not self.description.strip():
            raise ValueError("Risk description cannot be empty.")

        if self.mitigation is not None and not self.mitigation.strip():
            raise ValueError("Mitigation cannot be empty.")
