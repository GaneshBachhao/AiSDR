from app.application.common.operation_result import OperationResult


class AddSolutionValidator:
    def validate(
        self,
        command,
    ):

        result = OperationResult(success=True)

        if not command.recommendation_id:
            result.add_error("Recommendation id is required.")

        if not command.title:
            result.add_error("Solution title is required.")

        if not command.description:
            result.add_error("Solution description is required.")

        if not command.solution_type:
            result.add_error("Solution type is required.")

        if not command.priority:
            result.add_error("Solution priority is required.")

        return result
