from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class ExceptionMiddleware(BaseHTTPMiddleware):
    """
    Handles unexpected exceptions.
    """

    async def dispatch(self, request: Request, call_next):

        try:
            return await call_next(request)

        except Exception:
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "Internal Server Error",
                },
            )