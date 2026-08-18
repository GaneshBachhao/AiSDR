import traceback

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.application.common.exceptions.error_code import ErrorCode


class ExceptionMiddleware(BaseHTTPMiddleware):
    """
    Handles unexpected exceptions.

    `ApplicationException` subclasses (ValidationException,
    NotFoundException, ConflictException, UnauthorizedException, ...)
    never reach here -- Starlette's own exception-handler dispatch
    (registered via `register_application_exception_handlers`) intercepts
    those first and formats them with their real status code. This
    middleware is the fallback for everything else: a raw IntegrityError,
    an AIProviderException, a bug -- anything with no registered handler,
    which would otherwise propagate all the way to Starlette's default
    error response and break this app's `{success, message, error_code,
    details}` response contract.
    """

    async def dispatch(self, request: Request, call_next):

        try:
            return await call_next(request)

        except Exception:
            traceback.print_exc()

            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "Internal Server Error",
                    "error_code": ErrorCode.INTERNAL_ERROR.value,
                    "details": {},
                },
            )
