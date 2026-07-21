from app.ai.providers.gemini_provider import GeminiProvider


class AIService:

    def __init__(self):
        self.provider = GeminiProvider()

    def generate(
        self,
        prompt: str
    ) -> dict:
        """
        Future:
        - Prompt logging
        - Token counting
        - Cost tracking
        - Retry mechanism
        - Provider fallback
        """

        return self.provider.generate(prompt)