"""
Application Exceptions

Common exceptions used by the Application layer.
"""


class ApplicationException(Exception):
    """
    Base exception for all application-layer errors.
    """

    def __init__(
        self,
        message: str,
    ):
        super().__init__(message)


class ValidationException(ApplicationException):
    """
    Raised when application validation fails.
    """


class UseCaseExecutionException(ApplicationException):
    """
    Raised when a use case cannot complete successfully.
    """


class ResourceNotFoundException(ApplicationException):
    """
    Raised when a requested resource cannot be found.
    """


class ConflictException(ApplicationException):
    """
    Raised when an operation conflicts with existing state.
    """


class UnauthorizedException(ApplicationException):
    """
    Raised when the caller is not authorized.
    """


class ForbiddenException(ApplicationException):
    """
    Raised when the caller lacks permission.
    """