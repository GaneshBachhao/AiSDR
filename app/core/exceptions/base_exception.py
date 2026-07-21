"""
Base Exception Classes
"""


class AgneticAIException(Exception):
    """
    Base exception for the entire application.
    """

    def __init__(
        self,
        message: str,
    ):
        self.message = message
        super().__init__(message)


class ValidationException(AgneticAIException):
    """
    Raised when validation fails.
    """

    pass


class NotFoundException(AgneticAIException):
    """
    Raised when an entity cannot be found.
    """

    pass


class DuplicateException(AgneticAIException):
    """
    Raised when attempting to create a duplicate entity.
    """

    pass


class BusinessRuleException(AgneticAIException):
    """
    Raised when business rules are violated.
    """

    pass