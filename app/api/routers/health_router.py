"""
Health Router

Provides health and readiness endpoints for AiSDR.
"""

from datetime import UTC, datetime

from fastapi import APIRouter

from app.api.metadata import (
    API_TITLE,
    API_VERSION,
)

health_router = APIRouter(

    prefix="/health",

    tags=["Health"],

)


# ==========================================================
# Health
# ==========================================================

@health_router.get(
    "",
    summary="Application Health",
)
def health() -> dict:
    """
    Returns the overall application health.
    """

    return {

        "application": API_TITLE,

        "version": API_VERSION,

        "status": "healthy",

        "timestamp": datetime.now(UTC),

    }


# ==========================================================
# Liveness Probe
# ==========================================================

@health_router.get(
    "/live",
    summary="Liveness Probe",
)
def live() -> dict:
    """
    Kubernetes/Docker liveness probe.
    """

    return {

        "status": "alive",

    }


# ==========================================================
# Readiness Probe
# ==========================================================

@health_router.get(
    "/ready",
    summary="Readiness Probe",
)
def ready() -> dict:
    """
    Kubernetes/Docker readiness probe.

    Future enhancements:
    - Database connectivity
    - Redis connectivity
    - Gemini/OpenAI availability
    - SMTP availability
    """

    return {

        "status": "ready",

    }


# ==========================================================
# Version
# ==========================================================

@health_router.get(
    "/version",
    summary="Application Version",
)
def version() -> dict:
    """
    Returns application version.
    """

    return {

        "application": API_TITLE,

        "version": API_VERSION,

    }