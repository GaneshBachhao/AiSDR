"""
Configuration for the company_research module.

Follows the same pydantic-settings pattern as
``app.infrastructure.configuration.database_settings.DatabaseSettings``:
values are read from real process environment variables first, falling
back to a local ``.env`` file if present.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class CompanyResearchSettings(BaseSettings):
    """Tunables for the company-research discovery/research pipeline."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Discovery candidate pool sizing.
    candidate_pool_min: int = 20
    candidate_pool_max: int = 80
    candidate_pool_multiplier: int = 5

    # Bounded concurrency for per-candidate identity/evidence research.
    max_concurrent_research: int = 6

    # Evidence gathering.
    max_evidence_items: int = 8

    # Identity verification.
    min_identity_confidence: str = "MEDIUM"

    # Cheap-tier (directory) discovery: how long a sector/geography's mined
    # candidates are reused before re-querying Tavily.
    directory_cache_ttl_seconds: int = 3600
