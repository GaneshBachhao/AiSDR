from __future__ import annotations

from fastapi import APIRouter

from app.infrastructure.ai.composition import ai_config_diagnostics, default_ai_provider
from app.infrastructure.configuration.ai_provider_settings import AIProviderSettings
from app.presentation.schemas.responses.ai_config_diagnostics_response import (
    AIConfigDiagnosticsResponse,
    ProviderDiagnosticsSchema,
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get(
    "/ai-config",
    response_model=AIConfigDiagnosticsResponse,
    summary="Effective AI provider configuration",
)
async def get_ai_config_diagnostics() -> AIConfigDiagnosticsResponse:
    """
    Report the effective, resolved AI provider configuration.

    Never returns full API keys -- only a last-4-character fingerprint --
    and reports whether each key came from a real environment variable or
    only from ``.env``, so a shadowing environment variable is visible in
    one call instead of a manual investigation.
    """

    return AIConfigDiagnosticsResponse(
        default_provider=default_ai_provider(),
        fallback_order=AIProviderSettings().fallback_list(),
        providers=[
            ProviderDiagnosticsSchema.model_validate(diagnostics) for diagnostics in ai_config_diagnostics()
        ],
    )
