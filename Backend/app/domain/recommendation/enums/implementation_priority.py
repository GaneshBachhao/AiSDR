from enum import StrEnum


class ImplementationPriority(StrEnum):
    """
    Represents the implementation priority of a solution.
    """

    LOW = "Low"

    MEDIUM = "Medium"

    HIGH = "High"

    CRITICAL = "Critical"

    @classmethod
    def _missing_(
        cls,
        value: object,
    ) -> "ImplementationPriority | None":
        """
        Allow lookup by enum name or display value.
        """

        if isinstance(value, str):
            normalized = value.strip()

            member = cls.__members__.get(
                normalized.upper(),
            )
            if member is not None:
                return member

            for member in cls:
                if member.value.lower() == normalized.lower():
                    return member

        return None
