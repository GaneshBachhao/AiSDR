from enum import StrEnum


class SolutionType(StrEnum):
    """
    Represents the category of an AI solution.
    """

    AI_AGENT = "AI Agent"

    COPILOT = "Copilot"

    AUTOMATION = "Automation"

    ANALYTICS = "Analytics"

    CHATBOT = "Chatbot"

    KNOWLEDGE_ASSISTANT = "Knowledge Assistant"

    DOCUMENT_INTELLIGENCE = "Document Intelligence"

    PREDICTIVE_AI = "Predictive AI"

    CUSTOM = "Custom"

    @classmethod
    def _missing_(
        cls,
        value: object,
    ) -> "SolutionType | None":
        """
        Allow lookup by enum name or value.
        """

        if isinstance(
            value,
            str,
        ):
            normalized = value.strip()

            member = cls.__members__.get(
                normalized.upper(),
            )
            if member is not None:
                return member

            for member in cls:
                if member.value.lower() == normalized.lower():
                    return member

        return None