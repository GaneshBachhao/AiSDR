# tests/application/common/exceptions/test_application_exceptions.py

from app.application.common.exceptions import (
    ApplicationException,
    ErrorCode,
    ValidationException,
)
from app.application.common.exceptions.conflict_exception import (
    ConflictException,
)
from app.application.common.exceptions.forbidden_exception import (
    ForbiddenException,
)
from app.application.common.exceptions.not_found_exception import (
    NotFoundException,
)
from app.application.common.exceptions.unauthorized_exception import (
    UnauthorizedException,
)


def test_application_exception_properties() -> None:
    exception = ApplicationException(
        "Something failed.",
        error_code=ErrorCode.INTERNAL_ERROR,
        details={"key": "value"},
    )

    assert exception.message == "Something failed."
    assert exception.error_code is ErrorCode.INTERNAL_ERROR
    assert exception.details["key"] == "value"
    assert str(exception) == "Something failed."


def test_application_exception_to_dict() -> None:
    exception = ApplicationException(
        "Failure.",
        error_code=ErrorCode.CONFLICT,
        details={"resource": "lead"},
    )

    assert exception.to_dict() == {
        "message": "Failure.",
        "error_code": "CONFLICT",
        "details": {"resource": "lead"},
    }


def test_validation_exception() -> None:
    exception = ValidationException(
        "Validation failed.",
        details={"field": "email"},
    )

    assert exception.error_code is ErrorCode.VALIDATION_ERROR
    assert exception.details["field"] == "email"


def test_not_found_exception() -> None:
    exception = NotFoundException("Lead not found.")

    assert exception.error_code is ErrorCode.NOT_FOUND


def test_conflict_exception() -> None:
    exception = ConflictException("Lead already exists.")

    assert exception.error_code is ErrorCode.CONFLICT


def test_unauthorized_exception() -> None:
    exception = UnauthorizedException()

    assert exception.error_code is ErrorCode.UNAUTHORIZED
    assert exception.message == "Authentication required."


def test_forbidden_exception() -> None:
    exception = ForbiddenException()

    assert exception.error_code is ErrorCode.FORBIDDEN
    assert exception.message == "Access denied."


def test_exception_details_are_immutable() -> None:
    exception = ApplicationException(
        "Immutable.",
        details={"a": 1},
    )

    try:
        exception.details["a"] = 2  # type: ignore[index]
        assert False
    except TypeError:
        assert True