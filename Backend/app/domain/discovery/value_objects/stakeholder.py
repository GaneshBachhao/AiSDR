from dataclasses import dataclass


@dataclass(frozen=True)
class Stakeholder:
    """
    Value object representing a stakeholder involved
    in an AI discovery engagement.

    Stakeholders are identified by their role and influence
    within the organization, not by unique identity.
    """

    name: str

    designation: str

    department: str

    decision_maker: bool = False

    influence_level: int = 3

    def __post_init__(self) -> None:

        if not self.name.strip():
            raise ValueError(
                "Stakeholder name cannot be empty."
            )

        if not self.designation.strip():
            raise ValueError(
                "Stakeholder designation cannot be empty."
            )

        if not self.department.strip():
            raise ValueError(
                "Stakeholder department cannot be empty."
            )

        if not 1 <= self.influence_level <= 5:
            raise ValueError(
                "Influence level must be between 1 and 5."
            )