class WorkflowName:
    """
    Represents a valid workflow name.
    """

    MIN_LENGTH = 3
    MAX_LENGTH = 100

    def __init__(self, value: str):

        if not value:
            raise ValueError("Workflow name cannot be empty")

        value = value.strip()

        if len(value) < self.MIN_LENGTH:
            raise ValueError("Workflow name is too short")

        if len(value) > self.MAX_LENGTH:
            raise ValueError("Workflow name exceeds maximum length")

        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other) -> bool:

        if not isinstance(other, WorkflowName):
            return False

        return self._value == other.value

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return self._value
