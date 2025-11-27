# core/models/verification.py

"""
Verification Logs Model

This collection stores logs of every successful verification attempt.

Used for:
 - Admin analytics / statistics
 - Abuse monitoring
 - Debugging redirect server issues
 - Cleaning expired verify sessions
 - Allowing admin to check verification validity per user

Structure:
{
    user_id: 123456789,
    timestamp: <datetime>,
    hours: 1,                        # duration of verification
    expires: <datetime>
}
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class VerificationLog:
    """
    Represents ONE verification log entry.
    """

    user_id: int
    timestamp: datetime
    hours: int
    expires: datetime

    def to_dict(self):
        d = asdict(self)
        d["timestamp"] = self.timestamp
        d["expires"] = self.expires
        return d

    @staticmethod
    def from_dict(data: dict):
        return VerificationLog(
            user_id=data.get("user_id"),
            timestamp=data.get("timestamp", datetime.utcnow()),
            hours=data.get("hours", 1),
            expires=data.get("expires", datetime.utcnow())
        )

    @staticmethod
    def validate(data: dict) -> bool:
        """
        Checks minimal required structure.
        """
        return (
            "user_id" in data and
            "timestamp" in data and
            "expires" in data
        )

    @staticmethod
    def create(user_id: int, hours: int, expires: datetime):
        """
        Helper for consistent creation of log entries.
        """
        return VerificationLog(
            user_id=user_id,
            timestamp=datetime.utcnow(),
            hours=hours,
            expires=expires
        )
