from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.infrastructure.exceptions.infrastructure_exception import (
    InfrastructureException,
)


async def infrastructure_exception_handler(
    request: Request,
    exc: InfrastructureException,
) -> JSONResponse:
    """
    Handle infrastructure exceptions.
    """

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": str(exc),
        },
    )


def register_infrastructure_exception_handlers(app: FastAPI) -> None:
    """
    Register infrastructure exception handlers.
    """

    app.add_exception_handler(
        InfrastructureException,
        infrastructure_exception_handler,
    )