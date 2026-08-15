from app.application.recommendation.commands.submit_recommendation import (
    SubmitRecommendationCommand,
)


class SubmitRecommendationHandler:

    def __init__(
        self,
        repository,
        validator,
        mapper,
    ):
        self._repository = repository
        self._validator = validator
        self._mapper = mapper


    async def handle(
        self,
        command: SubmitRecommendationCommand,
    ):

        validation = self._validator.validate(
            command
        )

        if not validation.success:
            raise ValueError(
                validation.errors
            )


        recommendation = await self._repository.get_by_id(
            command.recommendation_id
        )


        if recommendation is None:
            raise ValueError(
                "Recommendation not found."
            )


        recommendation.submit()


        await self._repository.update(
            recommendation
        )


        return self._mapper.domain_to_dto(
            recommendation
        )