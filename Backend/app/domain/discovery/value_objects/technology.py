from dataclasses import dataclass


@dataclass(frozen=True)
class Technology:
    """
    Represents an existing technology used by the client.

    Captures the current technology landscape for AI readiness
    and integration assessment.
    """

    name: str

    category: str

    vendor: str | None = None

    version: str | None = None

    def __post_init__(self) -> None:

        if not self.name.strip():
            raise ValueError(
                "Technology name cannot be empty."
            )

        if not self.category.strip():
            raise ValueError(
                "Technology category cannot be empty."
            )