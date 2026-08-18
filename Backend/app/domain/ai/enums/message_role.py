from enum import Enum


class MessageRole(Enum):
    """
    Roles within an AI conversation.
    """

    SYSTEM = "SYSTEM"

    USER = "USER"

    ASSISTANT = "ASSISTANT"

    TOOL = "TOOL"
