# core/models/plans.py

"""
Premium Plans Model — structure for storing premium subscription plans.

Each plan defines:
 - number of premium days
 - price in INR
 - plan name / label
 - internal plan_id

Used by:
 - Admin Bot (add/edit/delete plans)
 - User Bot premium purchase flow
 - Order creation (plan_id stored inside each order)
 - Payment activation logic
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class PlanModel:
    """
    A premium plan entry.
    """

    plan_id: str             # unique ID like "plan_30d_40rs"
    name: str                # e.g., "30 DAYS"
    days: int                # number of subscription days
    price: float             # INR price
    created_at: datetime

    def to_dict(self):
        d = asdict(self)
        d["created_at"] = self.created_at
        return d

    @staticmethod
    def from_dict(data: dict):
        return PlanModel(
            plan_id=data.get("plan_id"),
            name=data.get("name", ""),
            days=int(data.get("days", 0)),
            price=float(data.get("price", 0)),
            created_at=data.get("created_at", datetime.utcnow())
        )

    @staticmethod
    def validate(data: dict) -> bool:
        """
        Basic schema validation.
        """
        required = ["plan_id", "name", "days", "price"]
        for key in required:
            if key not in data:
                return False
        return True

    @staticmethod
    def create(plan_id: str, name: str, days: int, price: float):
        """
        Helper for consistent creation of plan entries.
        """
        return PlanModel(
            plan_id=plan_id,
            name=name,
            days=days,
            price=price,
            created_at=datetime.utcnow()
        )
