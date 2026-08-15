from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """
    Handle FastAPI request validation errors.
    """

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation failed.",
            "errors": exc.errors(),
        },
    )


def register_validation_exception_handlers(app: FastAPI) -> None:
    """
    Register validation exception handlers.
    """

    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )