from fastapi import APIRouter, Depends

from app.presentation.api.dependencies.auth import get_current_user

from .admin_router import router as admin_router
from .assessment_router import router as assessment_router
from .auth_router import router as auth_router
from .company_research_router import router as company_research_router
from .company_router import router as company_router
from .compliance_router import router as compliance_router
from .contact_router import router as contact_router
from .discovery_router import router as discovery_router
from .health_router import router as health_router
from .lead_router import router as lead_router
from .outcome_router import router as outcome_router
from .qualification_router import router as qualification_router
from .recommendation_router import router as recommendation_router
from .sequence_router import router as sequence_router
from .suppression_router import router as suppression_router
from .webhook_router import router as webhook_router

api_router = APIRouter()

# Public -- no auth required. /auth/me self-protects via its own
# Depends(get_current_user) (see auth_router.py); /auth/login must be
# reachable by definition. webhook_router is also public -- a third-party
# caller can't carry a JWT bearer token -- but verifies its own
# shared-secret dependency instead (see dependencies/webhooks.py), so
# it's not actually unauthenticated, just not JWT-gated.
api_router.include_router(auth_router)
api_router.include_router(health_router)
api_router.include_router(webhook_router)

# Every other router is gated here, at the composition root, rather than
# per-router-file -- one place to audit, and no existing handler
# signatures need to change (the dependency's return value is discarded).
_protected = [Depends(get_current_user)]

api_router.include_router(admin_router, dependencies=_protected)
api_router.include_router(company_router, dependencies=_protected)
api_router.include_router(company_research_router, dependencies=_protected)
api_router.include_router(discovery_router, dependencies=_protected)
api_router.include_router(lead_router, dependencies=_protected)
api_router.include_router(contact_router, dependencies=_protected)
api_router.include_router(assessment_router, dependencies=_protected)
api_router.include_router(qualification_router, dependencies=_protected)
api_router.include_router(recommendation_router, dependencies=_protected)
api_router.include_router(suppression_router, dependencies=_protected)
api_router.include_router(compliance_router, dependencies=_protected)
api_router.include_router(outcome_router, dependencies=_protected)
api_router.include_router(sequence_router, dependencies=_protected)
