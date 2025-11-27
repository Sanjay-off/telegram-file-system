

# core/utils/time_utils.py

"""
Time Utilities
--------------

Provides consistent UTC datetime operations for:
 - Verification expiry
 - Premium expiry
 - Order expiry (QR expiry, confirm window)
 - Temporary message deletion
 - Cron jobs
 - Stats

No external dependencies.
"""

from datetime import datetime, timedelta, timezone


# ---------------------------------------------------------------------
# CURRENT TIME IN UTC
# ---------------------------------------------------------------------
def now() -> datetime:
    """
    Returns the current UTC datetime with tzinfo set.
    """
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------
# PARSE ISO STRING → DATETIME
# ---------------------------------------------------------------------
def parse_datetime(dt_str: str) -> datetime:
    """
    Parses ISO formatted datetime string into a UTC datetime object.
    """
    return datetime.fromisoformat(dt_str).astimezone(timezone.utc)


# ---------------------------------------------------------------------
# FORMAT DATETIME → READABLE STRING
# ---------------------------------------------------------------------
def format_datetime(dt: datetime) -> str:
    """
    Returns an easily readable timestamp for user-facing messages.
    Example: 2025-01-20 14:28 UTC
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M UTC")


# ---------------------------------------------------------------------
# ADD HOURS / MINUTES
# ---------------------------------------------------------------------
def add_hours(dt: datetime, hours: int) -> datetime:
    """
    Adds hours to a datetime object.
    """
    return dt + timedelta(hours=hours)


def add_minutes(dt: datetime, minutes: int) -> datetime:
    """
    Adds minutes to a datetime object.
    """
    return dt + timedelta(minutes=minutes)


# ---------------------------------------------------------------------
# CHECK IF EXPIRED
# ---------------------------------------------------------------------
def is_expired(dt: datetime) -> bool:
    """
    Returns True if given datetime is in the past.
    """
    return dt < now()


# ---------------------------------------------------------------------
# REMAINING TIME (for premium / verification)
# ---------------------------------------------------------------------
def remaining_time(expiry: datetime) -> dict:
    """
    Returns a dict with days/hours/minutes remaining until expiry.

    Example:
        {
            "days": 1,
            "hours": 5,
            "minutes": 23
        }
    """

    if expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=timezone.utc)

    remaining = expiry - now()

    if remaining.total_seconds() < 0:
        return {"days": 0, "hours": 0, "minutes": 0}

    days = remaining.days
    hours = remaining.seconds // 3600
    minutes = (remaining.seconds % 3600) // 60

    return {
        "days": days,
        "hours": hours,
        "minutes": minutes
    }
