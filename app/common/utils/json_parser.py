import json
import re

from app.core.logger import logger


class JsonParser:
    """
    Safely extracts and parses JSON returned by LLMs.
    """

    @staticmethod
    def parse(text: str) -> dict:
        """
        Extract JSON from an LLM response.

        Raises:
            ValueError if valid JSON cannot be extracted.
        """

        if not text:
            raise ValueError("Empty AI response.")

        cleaned = text.strip()

        # Remove markdown code fences
        cleaned = re.sub(
            r"^```(?:json)?",
            "",
            cleaned,
            flags=re.IGNORECASE | re.MULTILINE,
        )

        cleaned = re.sub(
            r"```$",
            "",
            cleaned,
            flags=re.MULTILINE,
        )

        # Find first JSON object
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start == -1 or end == -1:
            raise ValueError("No JSON object found.")

        cleaned = cleaned[start:end + 1]

        try:
            return json.loads(cleaned)

        except json.JSONDecodeError as ex:

            logger.exception(
                "Failed to parse AI JSON response."
            )

            raise ValueError(
                "Invalid JSON returned by AI."
            ) from ex