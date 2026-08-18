class DomainException(Exception):
    """
    Base exception for all domain-related business rule violations.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self._message = message

    @property
    def message(self) -> str:
        return self._message

    def __str__(self) -> str:
        return self._message
