from fastapi import FastAPI

from app.presentation.api.exception_handlers import register_exception_handlers
from app.presentation.api.middleware.correlation_id import CorrelationIdMiddleware
from app.presentation.api.middleware.exception import ExceptionMiddleware
from app.presentation.api.middleware.logging import LoggingMiddleware
from app.presentation.api.routers import api_router
from app.presentation.configuration import (
    configure_cors,
    configure_gzip,
    configure_openapi,
    configure_security,
    configure_trusted_hosts,
    configure_versioning,
)
from app.presentation.startup import lifespan


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """

    app = FastAPI(
        lifespan=lifespan,
    )

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    configure_openapi(app)
    configure_versioning(app)

    configure_cors(app)
    configure_gzip(app)
    configure_trusted_hosts(app)
    configure_security(app)

    # ------------------------------------------------------------------
    # Middleware
    # ------------------------------------------------------------------

    app.add_middleware(CorrelationIdMiddleware)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(ExceptionMiddleware)

    # ------------------------------------------------------------------
    # Exception Handlers
    # ------------------------------------------------------------------

    register_exception_handlers(app)

    # ------------------------------------------------------------------
    # Routers
    # ------------------------------------------------------------------

    app.include_router(api_router)

    return app


app = create_app()