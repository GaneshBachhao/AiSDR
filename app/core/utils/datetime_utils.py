"""
DateTime Utilities
"""

from datetime import datetime
from datetime import timezone


class DateTimeUtils:

    @staticmethod
    def utc_now() -> datetime:
        """
        Current UTC timestamp.
        """

        return datetime.now(
            timezone.utc,
        )

    @staticmethod
    def iso_timestamp() -> str:
        """
        ISO formatted UTC timestamp.
        """

        return (
            DateTimeUtils.utc_now()
            .isoformat()
        )