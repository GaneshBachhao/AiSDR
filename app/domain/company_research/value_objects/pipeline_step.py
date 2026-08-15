"""
Named steps in the per-candidate research pipeline, used to tag *where* an
unexpected failure happened -- Track 1 Phase 8 (EPIC-08, "Workflow
orchestration"). Only covers steps that make a real external call and can
therefore genuinely fail unpredictably (network/provider errors); the
deterministic gates in between (industry/size/enterprise matching) don't
need a step name because they don't fail, they just return a negative
result.
"""

from __future__ import annotations

from enum import StrEnum


class PipelineStep(StrEnum):
    IDENTITY_VERIFICATION = "identity_verification"
    EVIDENCE_GATHERING = "evidence_gathering"
    UNKNOWN = "unknown"
