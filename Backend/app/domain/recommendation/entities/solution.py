from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from app.domain.recommendation.enums.implementation_priority import (
    ImplementationPriority,
)
from app.domain.recommendation.enums.solution_type import SolutionType
from app.domain.recommendation.value_objects.business_benefit import (
    BusinessBenefit,
)
from app.domain.recommendation.value_objects.cost_estimate import (
    CostEstimate,
)
from app.domain.recommendation.value_objects.dependency import Dependency
from app.domain.recommendation.value_objects.expected_roi import ROI
from app.domain.recommendation.value_objects.implementation_risk import (
    ImplementationRisk,
)
from app.domain.recommendation.value_objects.technology_stack import (
    TechnologyStack,
)


@dataclass
class Solution:
    """
    Represents a proposed AI solution for addressing
    one or more assessment findings.
    """

    title: str

    description: str

    solution_type: SolutionType | str

    priority: ImplementationPriority | str = ImplementationPriority.MEDIUM

    technology_stack: list[TechnologyStack] = field(default_factory=list)

    business_benefits: list[BusinessBenefit] = field(default_factory=list)

    implementation_risks: list[ImplementationRisk] = field(default_factory=list)

    dependencies: list[Dependency] = field(default_factory=list)

    roi: ROI | None = None

    cost_estimate: CostEstimate | None = None

    solution_id: UUID = field(default_factory=uuid4)

    is_existing_offering: bool = True
    """Whether this is a real, existing Pamacore/AgneticAI service offering
    versus a generic, defensible industry opportunity suggested when no
    catalog entry fits. See docs/pamacore_aisdr_summary.md §7's labeling
    rule -- must always be surfaced distinctly, never blurred."""

    def __post_init__(self) -> None:

        if isinstance(self.solution_type, str):
            self.solution_type = SolutionType(self.solution_type)

        if isinstance(self.priority, str):
            self.priority = ImplementationPriority(self.priority)

    def add_technology(
        self,
        technology: TechnologyStack,
    ) -> None:
        """
        Add a technology to the solution stack.
        """
        self.technology_stack.append(technology)

    def add_business_benefit(
        self,
        benefit: BusinessBenefit,
    ) -> None:
        """
        Add an expected business benefit.
        """
        self.business_benefits.append(benefit)

    def add_risk(
        self,
        risk: ImplementationRisk,
    ) -> None:
        """
        Add an implementation risk.
        """
        self.implementation_risks.append(risk)

    def add_dependency(
        self,
        dependency: Dependency,
    ) -> None:
        """
        Add a prerequisite dependency.
        """
        self.dependencies.append(dependency)

    def update_roi(
        self,
        roi: ROI,
    ) -> None:
        """
        Update ROI estimation.
        """
        self.roi = roi

    def update_cost_estimate(
        self,
        cost_estimate: CostEstimate,
    ) -> None:
        """
        Update estimated implementation cost.
        """
        self.cost_estimate = cost_estimate
