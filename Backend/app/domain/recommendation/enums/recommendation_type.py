from enum import StrEnum


class RecommendationType(StrEnum):
    """
    Represents the type of AI recommendation.
    """

    AUTOMATION = "Automation"

    AI_AGENT = "AI Agent"

    CHATBOT = "Chatbot"

    RAG = "RAG"

    WORKFLOW = "Workflow"

    ANALYTICS = "Analytics"

    INTEGRATION = "Integration"

    DATA_PLATFORM = "Data Platform"

    CUSTOM = "Custom"