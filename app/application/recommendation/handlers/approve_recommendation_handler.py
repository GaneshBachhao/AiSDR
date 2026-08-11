from app.application.recommendation.commands.approve_recommendation import (
    ApproveRecommendationCommand,
)



class ApproveRecommendationHandler:

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
        command: ApproveRecommendationCommand,
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


        recommendation.approve()

        import inspect

        print("=" * 80)
        print("Repository object:", self._repository)
        print("Repository type:", type(self._repository))
        print("Repository id:", id(self._repository))
        print("Has update:", hasattr(self._repository, "update"))
        print("Dir contains update:", "update" in dir(self._repository))
        print("Methods:", [m for m in dir(self._repository) if "update" in m])
        print("Repository file:", inspect.getfile(type(self._repository)))
        print("=" * 80)

        await self._repository.update(recommendation)

    
        return self._mapper.domain_to_dto(
            recommendation
        )