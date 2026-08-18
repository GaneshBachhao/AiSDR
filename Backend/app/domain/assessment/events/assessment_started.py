from app.domain.shared.base import DomainEvent

from ..value_objects.assessment_id import AssessmentId


class AssessmentStarted(DomainEvent):
    """
    Raised when assessment starts.
    """

    def __init__(self, assessment_id: AssessmentId):
        super().__init__()
        self.assessment_id = assessment_id
