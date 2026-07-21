import time

from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start_time = time.time()

        logger.info("=" * 60)
        logger.info("Incoming Request")
        logger.info(f"Method : {request.method}")
        logger.info(f"URL    : {request.url.path}")

        response = await call_next(request)

        duration = time.time() - start_time

        logger.info("Request Completed")
        logger.info(f"Status : {response.status_code}")
        logger.info(f"Time   : {duration:.3f} sec")
        logger.info("=" * 60)

        return response