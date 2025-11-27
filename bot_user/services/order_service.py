# bot_user/services/order_service.py

from core.database import db
from core.utils.time_utils import now
from bot_admin.services.order_service import OrderService as AdminOrderService
from bot_admin.services.plan_service import PlanService


class UserOrderService:

    # ---------------------------------------------------------
    # GET ORDER (READ-ONLY FOR USER BOT)
    # ---------------------------------------------------------
    @staticmethod
    def get(order_id: str):
        """
        Fetch order using admin order service.
        Returns None if not found.
        """
        return AdminOrderService.get_order(order_id)

    # ---------------------------------------------------------
    # CHECK IF ORDER IS EXPIRED (QR EXPIRED)
    # ---------------------------------------------------------
    @staticmethod
    def is_expired(order_id: str) -> bool:
        """
        QR expiry check wrapper.
        """
        return AdminOrderService.is_order_expired(order_id)

    # ---------------------------------------------------------
    # CHECK IF CONFIRM WINDOW IS EXPIRED (10 hours)
    # ---------------------------------------------------------
    @staticmethod
    def is_confirm_window_expired(order_id: str) -> bool:
        """
        Checks if admin confirmation time has elapsed.
        """
        return AdminOrderService.is_confirm_window_expired(order_id)

    # ---------------------------------------------------------
    # GET PLAN DETAILS FOR THIS ORDER
    # ---------------------------------------------------------
    @staticmethod
    def get_plan(order) -> dict:
        """
        Returns premium plan document associated with an order.
        """
        plan_id = order.get("plan_id")
        if not plan_id:
            return None

        return PlanService.get_plan(plan_id)

    # ---------------------------------------------------------
    # CHECK IF ORDER IS PAID
    # ---------------------------------------------------------
    @staticmethod
    def is_paid(order: dict) -> bool:
        """
        Returns True if admin confirmed payment.
        """
        return order.get("status") == "paid"

    # ---------------------------------------------------------
    # GET UPI AMOUNT (including unique paise)
    # ---------------------------------------------------------
    @staticmethod
    def get_amount(order: dict) -> float:
        """
        Returns the final amount the user was asked to pay.
        """
        return float(order.get("amount", 0))

    # ---------------------------------------------------------
    # GET EXPIRY TIME
    # ---------------------------------------------------------
    @staticmethod
    def get_expiry(order: dict):
        """
        Returns expire timestamp (QR expiry).
        """
        return order.get("expires_at")

    # ---------------------------------------------------------
    # GET USER ID FROM ORDER
    # ---------------------------------------------------------
    @staticmethod
    def get_user_id(order: dict):
        return order.get("user_id")

    # ---------------------------------------------------------
    # IS CURRENT ORDER VALID FOR USER?
    # ---------------------------------------------------------
    @staticmethod
    def belongs_to_user(order: dict, user_id: int) -> bool:
        """
        Check if user requesting the order owns it.
        """
        return order.get("user_id") == user_id
