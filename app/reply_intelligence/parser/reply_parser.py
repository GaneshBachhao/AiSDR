"""
Reply Parser

Converts LLM output into ReplyAnalysis.
"""

import json
import re

from app.reply_intelligence.schemas.reply_analysis_schema import (
    ReplyAnalysis,
)


class ReplyParser:
    """
    Parses Gemini reply analysis responses.
    """

    @staticmethod
    def parse(
        text: str,
    ) -> ReplyAnalysis:

        if not text or not text.strip():
            raise ValueError("Empty LLM response.")

        text = text.strip()

        # Remove markdown fences
        text = re.sub(
            r"^```json",
            "",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(
            r"^```",
            "",
            text,
        )

        text = re.sub(
            r"```$",
            "",
            text,
        )

        # Extract JSON object
        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            raise ValueError(
                "No JSON object found."
            )

        payload = text[start:end + 1]

        data = json.loads(payload)

        return ReplyAnalysis.model_validate(data)