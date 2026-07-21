"""
FastAPI Application

Application entry point for AiSDR.

Responsibilities
----------------
- Create FastAPI application
- Configure OpenAPI metadata
- Register middleware
- Register exception handlers
- Register API routers
"""

from fastapi import FastAPI

from app.api.router import api_router
from app.api.metadata import (
    API_CONTACT,
    API_DESCRIPTION,
    API_LICENSE,
    API_TITLE,
    API_VERSION,
)


def create_application() -> FastAPI:
    """
    Creates and configures the FastAPI application.
    """

    app = FastAPI(

        title=API_TITLE,

        description=API_DESCRIPTION,

        version=API_VERSION,

        contact=API_CONTACT,

        license_info=API_LICENSE,

        docs_url="/docs",

        redoc_url="/redoc",

        openapi_url="/openapi.json",

    )

    # ---------------------------------------------------------
    # Routers
    # ---------------------------------------------------------

    app.include_router(
        api_router,
    )

    return app


app = create_application()


@app.get(
    "/",
    tags=["Root"],
)
def root() -> dict:
    """
    Root endpoint.
    """

    return {

        "application": API_TITLE,

        "version": API_VERSION,

        "status": "running",

    }