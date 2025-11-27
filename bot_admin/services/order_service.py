# bot_admin/services/order_service.py

from core.database import db
from core.utils.time_utils import now
from datetime import timedelta


class OrderService:

    # ---------------------------------------------------
    # CREATE NEW ORDER
    # ---------------------------------------------------
    @staticmethod
    def create_order(order_id: str, user_id: int, plan_id: str, amount: float, qr_expiry_minutes: int):
        """
        Create new payment order (pending)
        Used by Bot B when user selects a premium plan.
        """

        created_time = now()
        expires_at = created_time + timedelta(minutes=qr_expiry_minutes)
        confirm_until = created_time + timedelta(hours=10)  # 10 hour confirm window

        order_doc = {
            "order_id": order_id,
            "user_id": user_id,
            "plan_id": plan_id,
            "amount": amount,
            "status": "pending",
            "created_at": created_time,
            "expires_at": expires_at,
            "confirm_until": confirm_until,
            "paid_at": None
        }

        db.orders.insert_one(order_doc)
        return True

    # ---------------------------------------------------
    # GET ORDER
    # ---------------------------------------------------
    @staticmethod
    def get_order(order_id: str):
        """
        Fetch order by ID.
        """
        return db.orders.find_one({"order_id": order_id})

    # ---------------------------------------------------
    # LIST ORDERS
    # ---------------------------------------------------
    @staticmethod
    def list_orders(limit: int = 100):
        """
        Return latest orders.
        """
        return list(db.orders.find().sort("created_at", -1).limit(limit))

    @staticmethod
    def list_pending():
        return list(db.orders.find({"status": "pending"}).sort("created_at", -1).limit(100))

    @staticmethod
    def list_expired():
        return list(db.orders.find({"status": "expired"}).sort("created_at", -1).limit(100))

    @staticmethod
    def list_paid():
        return list(db.orders.find({"status": "paid"}).sort("paid_at", -1).limit(100))

    # ---------------------------------------------------
    # EXPIRE ORDER (QR expired)
    # ---------------------------------------------------
    @staticmethod
    def expire_order(order_id: str):
        """
        Mark order as expired.
        """
        db.orders.update_one(
            {"order_id": order_id},
            {"$set": {"status": "expired"}}
        )
        return True

    # ---------------------------------------------------
    # CHECK IF ORDER IS EXPIRED
    # ---------------------------------------------------
    @staticmethod
    def is_order_expired(order_id: str):
        order = OrderService.get_order(order_id)
        if not order:
            return True

        return now() > order["expires_at"]

    # ---------------------------------------------------
    # CHECK IF CONFIRM WINDOW IS EXPIRED (10 hours)
    # ---------------------------------------------------
    @staticmethod
    def is_confirm_window_expired(order_id: str):
        order = OrderService.get_order(order_id)
        if not order:
            return True

        return now() > order["confirm_until"]

    # ---------------------------------------------------
    # MARK ORDER AS PAID
    # ---------------------------------------------------
    @staticmethod
    def mark_as_paid(order_id: str):
        """
        Mark order as paid (manual admin confirmation).
        """
        db.orders.update_one(
            {"order_id": order_id},
            {"$set": {"status": "paid", "paid_at": now()}}
        )
        return True

    # ---------------------------------------------------
    # DELETE ORDER
    # ---------------------------------------------------
    @staticmethod
    def delete_order(order_id: str):
        """
        Remove an order permanently.
        """
        result = db.orders.delete_one({"order_id": order_id})
        return result.deleted_count > 0

    # ---------------------------------------------------
    # UPDATE ORDER STATUS
    # ---------------------------------------------------
    @staticmethod
    def update_status(order_id: str, status: str):
        """
        General status update function.
        """
        db.orders.update_one(
            {"order_id": order_id},
            {"$set": {"status": status}}
        )
        return True
