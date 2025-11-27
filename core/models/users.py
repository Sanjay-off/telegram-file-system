# core/models/users.py

"""
Users Model — unified storage for all end-user data.

Each Telegram user who interacts with Bot B (File Delivery Bot)
gets an entry in db.users.

Fields tracked:
 - user_id (Telegram ID)
 - username / full name (optional)
 - joined_at
 - verification state + expiry
 - premium state + expiry + plan_id
 - statistics-friendly structure
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class UserModel:
    """
    Represents a user document inside MongoDB.
    """

    user_id: int
    first_name: Optional[str]
    username: Optional[str]
    joined_at: datetime

    # Verification fields
    is_verified: bool
    verified_until: Optional[datetime]

    # Premium fields
    is_premium: bool
    premium_expiry: Optional[datetime]
    premium_plan: Optional[str]

    def to_dict(self):
        d = asdict(self)
        d["joined_at"] = self.joined_at
        d["verified_until"] = self.verified_until
        d["premium_expiry"] = self.premium_expiry
        return d

    @staticmethod
    def from_dict(data: dict):
        return UserModel(
            user_id=data.get("user_id"),
            first_name=data.get("first_name"),
            username=data.get("username"),
            joined_at=data.get("joined_at", datetime.utcnow()),

            is_verified=data.get("is_verified", False),
            verified_until=data.get("verified_until"),

            is_premium=data.get("is_premium", False),
            premium_expiry=data.get("premium_expiry"),
            premium_plan=data.get("premium_plan"),
        )

    @staticmethod
    def create(user_id: int, first_name: str = "", username: str = None):
        """
        Create a fresh user entry with default values.
        """
        return UserModel(
            user_id=user_id,
            first_name=first_name,
            username=username,
            joined_at=datetime.utcnow(),
            is_verified=False,
            verified_until=None,
            is_premium=False,
            premium_expiry=None,
            premium_plan=None
        )

    @staticmethod
    def validate(data: dict) -> bool:
        """
        Basic schema validation: ensure user_id exists.
        """
        return "user_id" in data
