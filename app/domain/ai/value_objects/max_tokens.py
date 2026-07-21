class MaxTokens:
    """
    Represents the maximum number of tokens.
    """

    def __init__(self, value: int):

        if value <= 0:
            raise ValueError(
                "Maximum tokens must be greater than zero."
            )

        self._value = value

    @property
    def value(self):
        return self._value

    def __eq__(self, other):
        return (
            isinstance(other, MaxTokens)
            and self.value == other.value
        )

    def __hash__(self):
        return hash(self._value)

    def __int__(self):
        return self._value