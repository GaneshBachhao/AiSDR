from __future__ import annotations

from dataclasses import dataclass

from app.domain.company_research.entities.candidate import CompanyCandidate
from app.domain.company_research.services.candidate_gate import DeterministicCandidateGate


@dataclass(slots=True)
class FunnelMetrics:
    discovered: int = 0
    deterministic_accepted: int = 0
    deterministic_rejected: int = 0
    deduplicated: int = 0
    verified: int = 0
    researched: int = 0


class DiscoveryFunnel:
    """Asymmetric funnel coordinator for the pre-verification boundary.

    Only normalized, deterministic-gate-approved candidates should cross into
    network identity verification and deeper research. This class intentionally
    has no database, search SDK, or LLM dependency — it is pure Domain logic
    over in-memory candidates.
    """

    def __init__(self, gate: DeterministicCandidateGate | None = None) -> None:
        self.gate = gate or DeterministicCandidateGate()

    def gate_candidates(
        self,
        candidates: list[CompanyCandidate],
    ) -> tuple[list[CompanyCandidate], FunnelMetrics]:
        metrics = FunnelMetrics(discovered=len(candidates))
        eligible = [candidate for candidate in candidates if self.gate.evaluate(candidate).accepted]
        accepted = self.gate.accept_unique(eligible)
        metrics.deterministic_rejected = len(candidates) - len(eligible)
        metrics.deduplicated = len(eligible) - len(accepted)
        metrics.deterministic_accepted = len(accepted)
        return accepted, metrics
