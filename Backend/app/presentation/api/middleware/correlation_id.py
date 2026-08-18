from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    Adds a correlation ID to every request.
    """

    HEADER_NAME = "X-Correlation-ID"

    async def dispatch(self, request: Request, call_next):

        correlation_id = request.headers.get(self.HEADER_NAME) or str(uuid4())

        request.state.correlation_id = correlation_id

        response = await call_next(request)

        response.headers[self.HEADER_NAME] = correlation_id

        return response
