"""Response schema for the AI config diagnostics endpoint."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ProviderDiagnosticsSchema(BaseModel):
    """Secret-safe configuration snapshot for one AI provider."""

    model_config = ConfigDict(from_attributes=True)

    provider: str
    configured: bool
    model: str
    key_fingerprint: str | None
    key_source: str
    second_key_configured: bool = False


class AIConfigDiagnosticsResponse(BaseModel):
    """Effective AI provider configuration, for troubleshooting only."""

    default_provider: str
    fallback_order: list[str]
    providers: list[ProviderDiagnosticsSchema]
