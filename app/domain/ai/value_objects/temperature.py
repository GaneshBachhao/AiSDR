class Temperature:
    """
    Represents AI generation temperature.
    """

    MIN = 0.0
    MAX = 2.0

    def __init__(self, value: float):

        if not (self.MIN <= value <= self.MAX):
            raise ValueError(
                f"Temperature must be between {self.MIN} and {self.MAX}."
            )

        self._value = float(value)

    @property
    def value(self):
        return self._value

    def __eq__(self, other):
        return (
            isinstance(other, Temperature)
            and self.value == other.value
        )

    def __hash__(self):
        return hash(self._value)

    def __float__(self):
        return self._value