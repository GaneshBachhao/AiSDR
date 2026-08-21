from enum import StrEnum


class ReplyClassification(StrEnum):
    """
    Category assigned to an inbound reply from a Lead's contact (EPIC-10.1).
    """

    INTERESTED = "Interested"

    NOT_NOW = "NotNow"

    OBJECTION = "Objection"

    UNSUBSCRIBE = "Unsubscribe"

    OUT_OF_OFFICE = "OutOfOffice"

    WRONG_PERSON = "WrongPerson"
