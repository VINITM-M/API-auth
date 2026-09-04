from datetime import datetime, timezone

def now() -> datetime:
    """Return the current time as a timezone-aware UTC datetime.

    The package stores every timestamp in UTC so that expiration and reset
    calculations stay correct regardless of the server's local timezone.

    Returns:
        datetime: The current moment, in UTC.

    """
    return datetime.now(timezone.utc)


def as_utc(value: datetime) -> datetime:
    """Return a timezone-aware UTC version of the given datetime.

    Naive datetimes (for example the ones some database drivers return) are
    assumed to already be expressed in UTC and are simply tagged as such.

    Args:
        value (datetime): The datetime to normalize.

    Returns:
        datetime: A timezone-aware datetime in UTC.

    """
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)