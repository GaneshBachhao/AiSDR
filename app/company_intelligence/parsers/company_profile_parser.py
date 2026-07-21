"""
Company Profile Parser

Converts raw LLM responses into a validated
CompanyProfile object.
"""

import json
import re

from pydantic import ValidationError

from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)


class CompanyProfileParser:
    """
    Parses LLM responses into CompanyProfile.
    """

    @staticmethod
    def parse(
        response: str,
    ) -> CompanyProfile:

        if not response:
            raise ValueError(
                "Empty response received from AI."
            )

        # Remove markdown fences
        cleaned = re.sub(
            r"```(?:json)?",
            "",
            response,
            flags=re.IGNORECASE,
        )

        cleaned = cleaned.replace(
            "```",
            "",
        ).strip()

        try:

            data = json.loads(cleaned)

        except json.JSONDecodeError as ex:

            raise ValueError(
                f"Invalid JSON returned by AI: {ex}"
            ) from ex

        try:

            return CompanyProfile.model_validate(data)

        except ValidationError as ex:

            raise ValueError(
                f"CompanyProfile validation failed: {ex}"
            ) from ex