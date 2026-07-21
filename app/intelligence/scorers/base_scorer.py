from abc import ABC
from abc import abstractmethod

from app.intelligence.common.schemas.evidence_schema import (
    Evidence,
)

from app.intelligence.common.schemas.score_result_schema import (
    ScoreResult,
)


class BaseScorer(ABC):

    @abstractmethod
    def score(
        self,
        evidence: list[Evidence],
    ) -> ScoreResult:
        raise NotImplementedError

    def normalize(
        self,
        value: float,
    ) -> float:
        return max(0, min(100, value))