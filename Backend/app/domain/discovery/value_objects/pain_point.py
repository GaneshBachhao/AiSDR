from dataclasses import dataclass


@dataclass(frozen=True)
class PainPoint:
    """
    Represents a business pain point identified during discovery.

    A pain point captures an operational challenge,
    its impact level, and affected business area.
    """

    title: str

    description: str

    severity: int

    department: str | None = None

    frequency: str | None = None

    def __post_init__(self) -> None:

        if not self.title.strip():
            raise ValueError("Pain point title cannot be empty.")

        if not self.description.strip():
            raise ValueError("Pain point description cannot be empty.")

        if not 1 <= self.severity <= 5:
            raise ValueError("Severity must be between 1 and 5.")
