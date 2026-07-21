from datetime import datetime, timezone


def utc_now() -> datetime:
    """
    Return the current UTC datetime.
    """
    return datetime.now(timezone.utc)


def normalize_datetime(dt: datetime | None) -> datetime | None:
    """
    Normalize datetimes loaded from the database.

    SQLite may return naive datetimes even when
    DateTime(timezone=True) is configured.

    If the datetime is naive, assume it represents UTC
    and attach the UTC timezone.
    """

    if dt is None:
        return None

    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)

    return dt