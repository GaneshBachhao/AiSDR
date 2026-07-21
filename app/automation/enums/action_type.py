"""
Automation Action Types

Actions produced by the automation engine.
"""

from enum import Enum


class ActionType(str, Enum):
    """
    Supported automation actions.
    """

    UPDATE_LEAD = "UPDATE_LEAD"

    UPDATE_CONVERSATION = "UPDATE_CONVERSATION"

    GENERATE_REPLY = "GENERATE_REPLY"

    SCHEDULE_FOLLOW_UP = "SCHEDULE_FOLLOW_UP"

    CREATE_MEETING = "CREATE_MEETING"

    NOTIFY_SALES = "NOTIFY_SALES"

    CLOSE_CONVERSATION = "CLOSE_CONVERSATION"

    NO_ACTION = "NO_ACTION"