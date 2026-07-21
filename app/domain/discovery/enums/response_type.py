from enum import StrEnum


class ResponseType(StrEnum):
    """
    Supported discovery response types.
    """

    TEXT = "Text"

    NUMBER = "Number"

    BOOLEAN = "Boolean"

    DATE = "Date"

    MULTI_SELECT = "Multi Select"

    FILE = "File"