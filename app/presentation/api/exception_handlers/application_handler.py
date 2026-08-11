from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.application.common.exceptions.application_exception import (
    ApplicationException,
)
from app.application.common.exceptions.error_code import ErrorCode


def _status_code_from_error_code(error_code: ErrorCode) -> int:
    if error_code == ErrorCode.VALIDATION_ERROR:
        return 422

    if error_code == ErrorCode.NOT_FOUND:
        return 404

    if error_code == ErrorCode.CONFLICT:
        return 409

    if error_code == ErrorCode.UNAUTHORIZED:
        return 401

    if error_code == ErrorCode.FORBIDDEN:
        return 403

    return 500


async def application_exception_handler(
    request: Request,
    exc: ApplicationException,
) -> JSONResponse:
    """
    Handle application-layer exceptions as structured API responses.
    """

    return JSONResponse(
        status_code=_status_code_from_error_code(exc.error_code),
        content={
            "success": False,
            "message": exc.message,
            "error_code": exc.error_code.value,
            "details": dict(exc.details),
        },
    )


def register_application_exception_handlers(app: FastAPI) -> None:
    """
    Register application exception handlers.
    """

    app.add_exception_handler(
        ApplicationException,
        application_exception_handler,
    )
