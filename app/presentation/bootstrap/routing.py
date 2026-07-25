from fastapi import FastAPI

from app.presentation.api.routers.ai_router import router as ai_router
from app.presentation.api.routers.assessment_router import router as assessment_router
from app.presentation.api.routers.discovery_router import router as discovery_router
from app.presentation.api.routers.health_router import router as health_router
from app.presentation.api.routers.lead_router import router as lead_router
from app.presentation.api.routers.recommendation_router import router as recommendation_router


def register_routers(
    app: FastAPI,
) -> None:
    """
    Register all API routers.
    """

    app.include_router(
        health_router,
    )

    app.include_router(
        lead_router,
    )

    app.include_router(
        discovery_router,
    )

    app.include_router(
        assessment_router,
    )

    app.include_router(
        recommendation_router,
    )

    app.include_router(
        ai_router,
    )