from app.domain.assessment.entities.assessment import Assessment
from app.domain.assessment.enums.maturity_level import MaturityLevel
from app.domain.assessment.value_objects.assessment_score import AssessmentScore


class AssessmentService:
    """
    Domain service for Assessment business operations.
    """

    @staticmethod
    def start(
        assessment: Assessment,
    ) -> None:
        """
        Start an assessment.
        """
        assessment.start()

    @staticmethod
    def complete(
        assessment: Assessment,
        summary: str | None = None,
    ) -> None:
        """
        Complete an assessment.
        """
        assessment.complete(summary)

    @staticmethod
    def update_score(
        assessment: Assessment,
        score: AssessmentScore,
    ) -> None:
        """
        Update assessment score.
        """
        assessment.update_score(score)

    @staticmethod
    def update_maturity(
        assessment: Assessment,
        maturity: MaturityLevel,
    ) -> None:
        """
        Update assessment maturity.
        """
        assessment.update_maturity(maturity)

    @staticmethod
    def calculate_score(
        assessment: Assessment,
    ) -> AssessmentScore:
        """
        Calculate the assessment score.

        Placeholder for future scoring engine.
        """
        return assessment.score

    @staticmethod
    def determine_maturity(
        score: AssessmentScore,
    ) -> MaturityLevel:
        """
        Determine maturity level based on score.

        Placeholder for future maturity model.
        """
        overall = score.overall_score

        if overall < 20:
            return MaturityLevel.INITIAL

        if overall < 40:
            return MaturityLevel.DEVELOPING

        if overall < 60:
            return MaturityLevel.DEFINED

        if overall < 80:
            return MaturityLevel.MANAGED

        return MaturityLevel.OPTIMIZED
