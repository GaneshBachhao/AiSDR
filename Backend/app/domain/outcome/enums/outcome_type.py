from enum import StrEnum


class OutcomeType(StrEnum):
    """
    What actually happened for a Lead after outreach.
    """

    MEETING_BOOKED = "Meeting Booked"

    WON = "Won"

    LOST = "Lost"

    NO_RESPONSE = "No Response"
