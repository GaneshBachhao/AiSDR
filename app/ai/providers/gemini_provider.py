from google import genai

from app.common.utils.json_parser import JsonParser
from app.core.config import settings
from app.core.logger import logger


class GeminiProvider:
    """
    Wrapper around Google's Gemini API.
    All Gemini-specific code lives here.
    """

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.AI_MODEL

    def generate(
        self,
        prompt: str,
    ) -> dict:
        """
        Generate structured JSON from Gemini.
        """

        logger.info(
            f"Generating AI response using model: {self.model}"
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return JsonParser.parse(
            response.text
        )