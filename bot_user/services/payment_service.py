# bot_user/services/payment_service.py

from core.database import db
from core.utils.time_utils import now
from bot_admin.services.order_service import OrderService
from bot_admin.services.plan_service import PlanService
from bot_admin.services.premium_service import PremiumService


class PaymentService:
    """
    Safe, read-only payment service for Bot B (User Bot).
    Admin Bot will always confirm the order.
    """

    # ---------------------------------------------------------
    # GET ORDER OBJECT
    # ---------------------------------------------------------
    @staticmethod
    def get_order(order_id: str):
        """
        Fetch order document or None.
        """
        return OrderService.get_order(order_id)

    # ---------------------------------------------------------
    # CHECK QR EXPIRY
    # ---------------------------------------------------------
    @staticmethod
    def qr_expired(order: dict) -> bool:
        """
        Returns True if QR code has expired.
        """
        if not order:
            return True
        return order["expires_at"] < now()

    # ---------------------------------------------------------
    # CHECK CONFIRM WINDOW (10 hour max)
    # ---------------------------------------------------------
    @staticmethod
    def confirm_window_expired(order: dict) -> bool:
        """
        Returns True if admin confirmation time is over.
        """
        if not order:
            return True
        return order["confirm_until"] < now()

    # ---------------------------------------------------------
    # CHECK IF ORDER BELONGS TO USER
    # ---------------------------------------------------------
    @staticmethod
    def belongs_to_user(order: dict, user_id: int) -> bool:
        """
        Prevents users from verifying another user's order.
        """
        if not order:
            return False
        return order["user_id"] == user_id

    # ---------------------------------------------------------
    # CHECK IF PAYMENT ALREADY CONFIRMED
    # ---------------------------------------------------------
    @staticmethod
    def is_paid(order: dict) -> bool:
        """
        True → admin confirmed payment.
        """
        if not order:
            return False
        return order.get("status") == "paid"

    # ---------------------------------------------------------
    # FETCH PLAN USED IN THIS ORDER
    # ---------------------------------------------------------
    @staticmethod
    def get_plan(order: dict):
        """
        Returns the plan document linked to this order.
        """
        if not order:
            return None
        return PlanService.get_plan(order["plan_id"])

    # ---------------------------------------------------------
    # ACTIVATES PREMIUM FOR USER (AFTER ADMIN CONFIRMATION)
    # ---------------------------------------------------------
    @staticmethod
    def activate_premium(order: dict):
        """
        This must run only after the admin confirms payment.
        """
        user_id = order["user_id"]
        plan_id = order["plan_id"]

        plan = PlanService.get_plan(plan_id)
        if not plan:
            return None

        days = plan["days"]

        # PremiumService handles automatic stacking
        expiry = PremiumService.activate_premium(
            user_id=user_id,
            plan_days=days,
            plan_id=plan_id
        )

        return expiry

    # ---------------------------------------------------------
    # GET UPI AMOUNT (final amount user must pay)
    # ---------------------------------------------------------
    @staticmethod
    def get_amount(order: dict) -> float:
        """
        Returns the final UPI amount including unique paise.
        """
        if not order:
            return 0
        return float(order["amount"])

    # ---------------------------------------------------------
    # FULL PAYMENT STATE MACHINE SUMMARY
    # ---------------------------------------------------------
    @staticmethod
    def get_payment_state(order: dict) -> str:
        """
        Returns: 'not_found', 'expired', 'paid', 'pending', 'confirm_window_expired'
        """

        if not order:
            return "not_found"

        # QR expired
        if PaymentService.qr_expired(order):
            return "expired"

        # Already paid
        if order["status"] == "paid":
            return "paid"

        # Pending BUT confirm window expired (10 hours)
        if PaymentService.confirm_window_expired(order):
            return "confirm_window_expired"

        # Still pending normally
        return "pending"
