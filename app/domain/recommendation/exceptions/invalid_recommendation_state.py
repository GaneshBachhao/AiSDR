from .recommendation_exception import RecommendationException


class InvalidRecommendationState(RecommendationException):
    """
    Raised when an invalid recommendation state transition is attempted.
    """

    pass