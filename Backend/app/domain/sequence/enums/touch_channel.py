from enum import StrEnum


class TouchChannel(StrEnum):
    """
    Delivery channel for one touch in a Sequence.
    """

    EMAIL = "Email"

    LINKEDIN = "LinkedIn"

    CALL_TASK = "Call Task"
