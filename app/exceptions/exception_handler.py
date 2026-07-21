from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.common.response import ApiResponse
from app.core.logger import logger
from app.exceptions.custom_exceptions import AgneticAIException


async def agnetic_exception_handler(
    request: Request,
    exc: AgneticAIException
):
    """
    Handles all custom AgneticAI exceptions.
    """

    logger.warning(
        f"{request.method} {request.url.path} -> {exc.message}"
    )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ApiResponse.error(
            message=exc.message
        )
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception
):
    """
    Handles all unhandled exceptions.
    """

    logger.exception(
        f"Unhandled exception on {request.method} {request.url.path}: {str(exc)}"
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ApiResponse.error(
            message="Internal Server Error"
        )
    )