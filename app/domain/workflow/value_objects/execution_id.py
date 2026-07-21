from uuid import UUID


class ExecutionId:
    """
    Unique identifier for workflow execution.
    """

    def __init__(self, value: UUID):

        if not isinstance(value, UUID):
            raise ValueError(
                "ExecutionId must be a UUID"
            )

        self._value = value


    @property
    def value(self) -> UUID:
        return self._value


    def __eq__(self, other) -> bool:
        if not isinstance(other, ExecutionId):
            return False

        return self._value == other.value


    def __hash__(self) -> int:
        return hash(self._value)


    def __str__(self) -> str:
        return str(self._value)