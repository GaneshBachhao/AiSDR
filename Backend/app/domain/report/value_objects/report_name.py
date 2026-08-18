class ReportName:
    """
    Represents a validated report name.
    """

    MIN_LENGTH = 3
    MAX_LENGTH = 150

    def __init__(self, value: str):

        if not value:
            raise ValueError("Report name cannot be empty.")

        value = value.strip()

        if len(value) < self.MIN_LENGTH:
            raise ValueError("Report name is too short.")

        if len(value) > self.MAX_LENGTH:
            raise ValueError("Report name exceeds maximum length.")

        self._value = value

    @property
    def value(self):
        return self._value

    def __eq__(self, other):
        return isinstance(other, ReportName) and self._value == other.value

    def __hash__(self):
        return hash(self._value)

    def __str__(self):
        return self._value
