class ModelName:
    """
    Represents an AI model identifier.
    """

    MIN_LENGTH = 2
    MAX_LENGTH = 100

    def __init__(self, value: str):

        value = value.strip()

        if len(value) < self.MIN_LENGTH:
            raise ValueError("Model name is too short.")

        if len(value) > self.MAX_LENGTH:
            raise ValueError("Model name is too long.")

        self._value = value

    @property
    def value(self):
        return self._value

    def __eq__(self, other):
        return (
            isinstance(other, ModelName)
            and self.value == other.value
        )

    def __hash__(self):
        return hash(self._value)

    def __str__(self):
        return self._value