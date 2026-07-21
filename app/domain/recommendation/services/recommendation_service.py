from app.domain.recommendation.entities.recommendation import (
    Recommendation,
)


class RecommendationService:
    """
    Domain service for Recommendation business operations.
    """

    @staticmethod
    def approve(
        recommendation: Recommendation,
    ) -> None:
        """
        Approve a recommendation.
        """
        recommendation.approve()

    @staticmethod
    def reject(
        recommendation: Recommendation,
    ) -> None:
        """
        Reject a recommendation.
        """
        recommendation.reject()

    @staticmethod
    def archive(
        recommendation: Recommendation,
    ) -> None:
        """
        Archive a recommendation.
        """
        recommendation.archive()