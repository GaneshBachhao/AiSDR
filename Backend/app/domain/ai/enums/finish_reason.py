from enum import Enum


class FinishReason(Enum):
    """
    Reason why AI generation finished.
    """

    STOP = "STOP"

    LENGTH = "LENGTH"

    TOOL_CALL = "TOOL_CALL"

    CONTENT_FILTER = "CONTENT_FILTER"

    ERROR = "ERROR"
