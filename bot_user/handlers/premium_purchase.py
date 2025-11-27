# bot_user/handlers/premium_purchase.py

from aiogram import Router, types
from aiogram.filters import CommandStart
from datetime import timedelta
from core.database import db
from core.utils.time_utils import now
from core.config import config
from bot_admin.utils.helpers import generate_order_id
from bot_admin.services.plan_service import PlanService
from bot_admin.services.order_service import OrderService
from bot_user.keyboards.inline_buttons import (
    premium_plans_keyboard,
    premium_qr_keyboard,
    premium_back_keyboard,
    payment_verify_keyboard
)

router = Router()

# ================================================================
# STEP 1 — USER CLICKS "GET PREMIUM" (from verify screen)
# ================================================================
@router.callback_query(lambda c: c.data.startswith("getpremium_"))
async def premium_start_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    # Fetch all premium plans
    plans = PlanService.list_plans()

    if not plans:
        return await callback.message.edit_text(
            "⚠ No premium plans configured.\nPlease contact admin.",
            parse_mode="Markdown"
        )

    # Show premium plan buttons
    await callback.message.edit_text(
        "💎 **PREMIUM PLANS**\n\nSelect your preferred plan:",
        reply_markup=premium_plans_keyboard(plans),
        parse_mode="Markdown"
    )


# ================================================================
# STEP 2 — USER SELECTS A PLAN  (callback: buyplan_<plan_id>)
# ================================================================
@router.callback_query(lambda c: c.data.startswith("buyplan_"))
async def choose_plan(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    _, plan_id = callback.data.split("_", 1)

    plan = PlanService.get_plan(plan_id)
    if not plan:
        return await callback.message.edit_text("❌ Plan no longer exists.")

    amount = plan["price"]
    days = plan["days"]

    # Generate new order_id
    order_id = generate_order_id()

    # QR expiry time from DB
    qr_setting = db.settings.find_one({"key": "qr_expiry"})
    qr_expiry_minutes = qr_setting["value"] if qr_setting else 10

    # Create order
    OrderService.create_order(
        order_id=order_id,
        user_id=user_id,
        plan_id=plan_id,
        amount=amount,
        qr_expiry_minutes=qr_expiry_minutes
    )

    # Generate UPI QR LINK
    upi_doc = db.settings.find_one({"key": "upi_id"})
    name_doc = db.settings.find_one({"key": "upi_name"})
    upi_id = upi_doc["value"] if upi_doc else "no_upi_set@upi"
    pay_name = name_doc["value"] if name_doc else "ADMIN"

    # Unique price?
    unique_mode = db.settings.find_one({"key": "unique_paise"})
    unique_on = unique_mode["value"] == "on" if unique_mode else False

    if unique_on:
        # Example: 40.23 / 40.87 etc
        paise_variation = int(str(user_id)[-2:])  # 0–99 variation
        amount = float(f"{int(amount)}.{paise_variation}")

    # Create QR string (UPI deep-link)
    upi_url = (
        f"upi://pay?"
        f"pa={upi_id}&"
        f"pn={pay_name}&"
        f"am={amount}&"
        f"cu=INR&"
        f"tr={order_id}&"
        f"tn=Order:{order_id}"
    )

    # QR expiry timestamp
    expiry_time = now() + timedelta(minutes=qr_expiry_minutes)

    # Show QR payment screen
    await callback.message.edit_text(
        f"💎 **PREMIUM PURCHASE**\n\n"
        f"🆔 Order ID: `{order_id}`\n"
        f"📦 Plan: `{days} DAYS`\n"
        f"💰 Amount: `₹{amount}`\n\n"
        f"⌛ QR Expires In: `{qr_expiry_minutes} minutes`\n\n"
        "Scan the QR or tap the button to pay:",
        reply_markup=premium_qr_keyboard(upi_url, order_id),
        parse_mode="Markdown"
    )


# ================================================================
# STEP 3 — USER PRESSES "VERIFY PAYMENT"
# ================================================================
@router.callback_query(lambda c: c.data.startswith("verifyorder_"))
async def verify_payment(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    _, order_id = callback.data.split("_", 1)

    order = OrderService.get_order(order_id)
    if not order:
        return await callback.message.edit_text("❌ Order not found.")

    # Check QR expiry
    if OrderService.is_order_expired(order_id):
        return await callback.message.edit_text(
            "⛔ **QR Code Expired**\n\n"
            "Please generate a new payment request.",
            reply_markup=premium_back_keyboard(),
            parse_mode="Markdown"
        )

    # Auto-confirm OFF → Manual confirmation only
    msg = await callback.message.answer(
        "⏳ Checking payment...\nThis may take 10–15 minutes...",
        parse_mode="Markdown"
    )

    # Delete after 3 seconds
    await asyncio.sleep(3)
    try:
        await msg.delete()
    except:
        pass

    # New message as per your design:
    # If user continuously presses "Verify Payment"
    # → Replace previous verification message
    return await callback.message.edit_text(
        "📨 **If you have paid, your order will be confirmed within 10 hours.**\n\n"
        f"🆔 Order ID: `{order_id}`",
        reply_markup=payment_verify_keyboard(order_id),
        parse_mode="Markdown"
    )


# ================================================================
# STEP 4 — USER PRESSES BACK BUTTON (premium_back)
# ================================================================
@router.callback_query(lambda c: c.data == "premium_back")
async def premium_back(callback: types.CallbackQuery):

    plans = PlanService.list_plans()
    if not plans:
        return await callback.message.edit_text(
            "⚠ No premium plans available.",
            parse_mode="Markdown"
        )

    await callback.message.edit_text(
        "💎 **PREMIUM PLANS**\n\nSelect your plan:",
        reply_markup=premium_plans_keyboard(plans),
        parse_mode="Markdown"
    )
