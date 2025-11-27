# bot_user/handlers/qr_generator.py

from datetime import timedelta
from core.database import db
from core.utils.time_utils import now
from core.config import config
from bot_admin.utils.helpers import generate_order_id
from bot_admin.services.plan_service import PlanService
from bot_admin.services.order_service import OrderService


async def generate_upi_qr(user_id: int, plan_id: str):
    """
    Generates a UPI QR Link + creates order in DB.
    Returns:
        order_id,
        amount,
        expiry_minutes,
        upi_url
    """

    # ---------------------------
    # PLAN VALIDATION
    # ---------------------------
    plan = PlanService.get_plan(plan_id)
    if not plan:
        return None, None, None, None

    amount = plan["price"]

    # ---------------------------
    # UNIQUE PRICE MODE
    # ---------------------------
    unique_mode = db.settings.find_one({"key": "unique_paise"})
    unique_on = unique_mode["value"] == "on" if unique_mode else False

    if unique_on:
        # Example: 40.23 / 40.87 / 40.51
        paise_variation = int(str(user_id)[-2:])  # last 2 digits 00–99
        amount = float(f"{int(amount)}.{paise_variation}")

    # ---------------------------
    # CREATE ORDER
    # ---------------------------
    order_id = generate_order_id()

    qr_setting = db.settings.find_one({"key": "qr_expiry"})
    qr_expiry_minutes = qr_setting["value"] if qr_setting else 10

    OrderService.create_order(
        order_id=order_id,
        user_id=user_id,
        plan_id=plan_id,
        amount=amount,
        qr_expiry_minutes=qr_expiry_minutes
    )

    # ---------------------------
    # UPI SETTINGS
    # ---------------------------
    upi_doc = db.settings.find_one({"key": "upi_id"})
    name_doc = db.settings.find_one({"key": "upi_name"})

    upi_id = upi_doc["value"] if upi_doc else "no_upi_set@upi"
    pay_name = name_doc["value"] if name_doc else "ADMIN"

    # ---------------------------
    # GENERATE UPI PAY URL
    # ---------------------------
    upi_url = (
        f"upi://pay?"
        f"pa={upi_id}&"
        f"pn={pay_name}&"
        f"am={amount}&"
        f"cu=INR&"
        f"tr={order_id}&"
        f"tn=Order:{order_id}"
    )

    return order_id, amount, qr_expiry_minutes, upi_url
