import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.infrastructure.logging.logger import get_logger


logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs incoming requests and outgoing responses.
    """

    async def dispatch(self, request: Request, call_next):

        start = time.perf_counter()

        response = await call_next(request)

        elapsed = (time.perf_counter() - start) * 1000

        logger.info(
            "%s %s %s %.2f ms",
            request.method,
            request.url.path,
            response.status_code,
            elapsed,
        )

        return response