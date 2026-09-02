from datetime import datetime
from zoneinfo import ZoneInfo


DEFAULT_TIMEZONE = "Asia/Kolkata"


def now_in_timezone(timezone_name: str = DEFAULT_TIMEZONE) -> datetime:
    """
    Return the current date and time for the given IANA timezone.

    Example:
        Asia/Kolkata
        America/New_York
        Europe/London
    """
    return datetime.now(ZoneInfo(timezone_name))


def india_now() -> datetime:
    """
    Return current India time.

    Kept as a convenience helper for places where
    India time is explicitly required.
    """
    return now_in_timezone(DEFAULT_TIMEZONE)