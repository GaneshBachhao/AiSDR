"""
API Router

Registers all API routers for the AiSDR application.
"""

from fastapi import APIRouter

from app.api.routers.health_router import health_router
from app.api.routers.discovery_router import discovery_router
from app.api.routers.company_intelligence_router import (
    company_intelligence_router,
)
from app.api.routers.qualification_router import (
    qualification_router,
)
from app.api.routers.recommendation_router import (
    recommendation_router,
)
from app.api.routers.lead_router import lead_router
from app.api.routers.contact_router import contact_router
from app.api.routers.email_router import email_router
from app.api.routers.pipeline_router import pipeline_router


api_router = APIRouter()


# ==========================================================
# Health
# ==========================================================

api_router.include_router(
    health_router,
)

# ==========================================================
# Discovery
# ==========================================================

api_router.include_router(
    discovery_router,
)

# ==========================================================
# Company Intelligence
# ==========================================================

api_router.include_router(
    company_intelligence_router,
)

# ==========================================================
# Qualification
# ==========================================================

api_router.include_router(
    qualification_router,
)

# ==========================================================
# Recommendation
# ==========================================================

api_router.include_router(
    recommendation_router,
)

# ==========================================================
# Lead
# ==========================================================

api_router.include_router(
    lead_router,
)

# ==========================================================
# Contact
# ==========================================================

api_router.include_router(
    contact_router,
)

# ==========================================================
# Email
# ==========================================================

api_router.include_router(
    email_router,
)

# ==========================================================
# Pipeline
# ==========================================================

api_router.include_router(
    pipeline_router,
)