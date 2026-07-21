from .assessment_exception import AssessmentException


class InvalidAssessmentState(AssessmentException):
    """
    Raised when an invalid assessment state transition is attempted.
    """

    pass