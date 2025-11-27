# core/models/orders.py

"""
Orders Model — structure for premium purchase orders.

Every premium plan purchase creates ONE order.

Used by:
 - bot_admin/services/order_service.py
 - bot_user/services/payment_service.py
 - bot_user/handlers/premium_purchase.py
 - bot_user/handlers/verify_payment.py
 - jobs/cleanup_expired_orders.py
 - Admin dashboard (stats)

The order lifecycle:
 1. created      → user opens QR screen
 2. pending      → user hasn't paid or admin not confirmed
 3. paid         → admin confirms (premium activated)
 4. expired      → QR expiry or confirm window flowed out
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class OrderModel:
    """
    Represents a premium purchase order.
    """

    order_id: str             # UNIQUE identifier (e.g., AA-2838196364-261125WES)
    user_id: int              # TG user ID of buyer
    plan_id: str              # Which premium plan they chose
    amount: float             # Final UPI amount (with unique paise if enabled)
    status: str               # 'pending' | 'paid' | 'expired'
    created_at: datetime      # Time of order creation
    expires_at: datetime      # QR code expiry time
    confirm_until: datetime   # Deadline for admin confirmation

    def to_dict(self):
        d = asdict(self)
        d["created_at"] = self.created_at
        d["expires_at"] = self.expires_at
        d["confirm_until"] = self.confirm_until
        return d

    @staticmethod
    def from_dict(data: dict):
        return OrderModel(
            order_id=data.get("order_id"),
            user_id=data.get("user_id"),
            plan_id=data.get("plan_id"),
            amount=float(data.get("amount", 0)),
            status=data.get("status", "pending"),
            created_at=data.get("created_at", datetime.utcnow()),
            expires_at=data.get("expires_at", datetime.utcnow()),
            confirm_until=data.get("confirm_until", datetime.utcnow())
        )

    @staticmethod
    def validate(data: dict) -> bool:
        required = [
            "order_id",
            "user_id",
            "plan_id",
            "amount",
            "created_at",
            "expires_at",
            "confirm_until"
        ]
        for key in required:
            if key not in data:
                return False
        return True

    @staticmethod
    def create(
        order_id: str,
        user_id: int,
        plan_id: str,
        amount: float,
        expires_at: datetime,
        confirm_until: datetime
    ):
        """
        Helper to create a new order model in a clean, consistent format.
        """
        return OrderModel(
            order_id=order_id,
            user_id=user_id,
            plan_id=plan_id,
            amount=amount,
            status="pending",
            created_at=datetime.utcnow(),
            expires_at=expires_at,
            confirm_until=confirm_until
        )
