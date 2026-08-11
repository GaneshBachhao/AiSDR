from datetime import UTC, datetime

from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "",
    summary="Health Check",
)
async def health_check() -> dict:
    """
    Application health check.
    """

    return {
        "status": "healthy",
        "service": "PamaCore Labs API",
        "version": "1.0.0",
        "timestamp": datetime.now(UTC).isoformat(),
    }