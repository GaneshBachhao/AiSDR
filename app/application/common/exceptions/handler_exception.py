from typing import Any, Optional


class HandlerException(Exception):
    """
    Base exception for application handler failures.

    All application layer specific exceptions
    should inherit from this class.
    """

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(message)

        self.message = message
        self.error_code = error_code
        self.details = details or {}


    def to_dict(self) -> dict[str, Any]:
        """
        Converts exception into a serializable format.
        """
        return {
            "message": self.message,
            "error_code": self.error_code,
            "details": self.details,
        }


class ValidationHandlerException(HandlerException):
    """
    Raised when application validation fails.
    """

    def __init__(
        self,
        message: str,
        errors: list[str],
    ):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            details={
                "errors": errors
            },
        )


class BusinessRuleHandlerException(HandlerException):
    """
    Raised when a business rule prevents execution.
    """

    def __init__(
        self,
        message: str,
        error_code: str = "BUSINESS_RULE_ERROR",
    ):
        super().__init__(
            message=message,
            error_code=error_code,
        )


class HandlerExecutionException(HandlerException):
    """
    Raised when unexpected execution failure occurs.
    """

    def __init__(
        self,
        message: str,
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code="HANDLER_EXECUTION_ERROR",
            details=details,
        )