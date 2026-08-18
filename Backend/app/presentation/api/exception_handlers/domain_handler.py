from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.shared.exceptions.domain_exception import DomainException


async def domain_exception_handler(
    request: Request,
    exc: DomainException,
) -> JSONResponse:
    """
    Handle domain exceptions.
    """

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": str(exc),
        },
    )


def register_domain_exception_handlers(app: FastAPI) -> None:
    """
    Register domain exception handlers.
    """

    app.add_exception_handler(
        DomainException,
        domain_exception_handler,
    )
