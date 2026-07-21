"""
Pipeline Context

Shared context passed between all pipeline stages.
"""

from datetime import datetime, UTC
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)

from app.discovery.schemas.discovery_schema import (
    DiscoveryRequest,
)

from app.lead_intelligence.qualification.schemas.qualification_result_schema import (
    QualificationResult,
)

from app.lead_intelligence.schemas.lead_candidate_schema import (
    LeadCandidate,
)

from app.models.lead import Lead
from app.models.contact import Contact
from app.models.email import Email

from app.ai.schemas.generated_email_schema import (
    GeneratedEmail,
)

from app.recommendation.schemas.recommendation_schema import (
    RecommendationResponse,
)

from app.emails.schemas.email_send_result_schema import (
    EmailSendResult,
)


class PipelineContext(BaseModel):
    """
    Shared context passed between every pipeline stage.

    Each stage reads from and writes to this object.
    """

    # ==========================================================
    # Pydantic Configuration
    # ==========================================================

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    # ==========================================================
    # Execution Information
    # ==========================================================

    execution_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    started_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    finished_at: datetime | None = None

    duration_ms: float | None = None

    status: str = "RUNNING"

    current_stage: str | None = None

    completed_stages: list[str] = Field(
        default_factory=list,
    )

    # ==========================================================
    # Pipeline Input
    # ==========================================================

    request: DiscoveryRequest | None = None

    # ==========================================================
    # Infrastructure
    # ==========================================================

    db: Session | None = None

    # ==========================================================
    # Discovery
    # ==========================================================

    candidate: LeadCandidate | None = None

    # ==========================================================
    # Company Intelligence
    # ==========================================================

    company_profile: CompanyProfile | None = None

    # ==========================================================
    # Qualification
    # ==========================================================

    qualification: QualificationResult | None = None

    # ==========================================================
    # Lead
    # ==========================================================

    lead: Lead | None = None

    # ==========================================================
    # Contacts
    # ==========================================================

    primary_contact: Contact | None = None

    contacts: list[Contact] = Field(
        default_factory=list,
    )

    # ==========================================================
    # AI Recommendations
    # ==========================================================

    recommendations: RecommendationResponse | None = None

    # ==========================================================
    # AI Generated Email
    # ==========================================================

    generated_email: GeneratedEmail | None = None

    # ==========================================================
    # Persisted Email
    # ==========================================================

    email: Email | None = None

    # ==========================================================
    # Email Provider Result
    # ==========================================================

    email_send_result: EmailSendResult | None = None

    # ==========================================================
    # Diagnostics
    # ==========================================================

    errors: list[str] = Field(
        default_factory=list,
    )

    warnings: list[str] = Field(
        default_factory=list,
    )

    # ==========================================================
    # Stage Results
    # ==========================================================

    stage_results: dict[str, object] = Field(
        default_factory=dict,
    )

    # ==========================================================
    # Metadata
    # ==========================================================

    metadata: dict[str, object] = Field(
        default_factory=dict,
    )