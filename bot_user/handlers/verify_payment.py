# bot_user/handlers/verify_payment.py

import asyncio
from aiogram import Router, types
from aiogram.filters import CommandStart
from core.database import db
from core.utils.time_utils import now
from bot_admin.services.order_service import OrderService
from bot_admin.services.premium_service import PremiumService
from bot_admin.services.plan_service import PlanService
from bot_user.keyboards.inline_buttons import (
    payment_verify_keyboard,
    premium_back_keyboard
)

router = Router()


# ================================================================
# 1️⃣ USER RETURNS WITH DEEPLINK → /start pay_<order_id>
# ================================================================
@router.message(CommandStart(deep_link_prefix="pay_"))
async def deeplink_payment_handler(message: types.Message):
    """
    Handles deep-link: /start pay_<order_id>
    For users returning from external UPI apps.
    """

    order_id = message.text.replace("/start ", "").replace("pay_", "")
    return await show_payment_state(message, order_id)



# ================================================================
# 2️⃣ CALLBACK: user clicks "VERIFY PAYMENT"
# ================================================================
@router.callback_query(lambda c: c.data.startswith("verifypay_"))
async def verify_payment_callback(callback: types.CallbackQuery):
    _, order_id = callback.data.split("_", 1)
    return await show_payment_state(callback.message, order_id)



# ================================================================
# MAIN PAYMENT VERIFICATION STATE MACHINE
# ================================================================
async def show_payment_state(message: types.Message, order_id: str):
    user_id = message.from_user.id
    order = OrderService.get_order(order_id)

    # ----------------------------------------------------
    # ORDER DOESN'T EXIST
    # ----------------------------------------------------
    if not order:
        return await message.answer(
            "❌ **Order Not Found**\nPlease try again.",
            parse_mode="Markdown"
        )

    # ----------------------------------------------------
    # ORDER EXPIRED (QR EXPIRED)
    # ----------------------------------------------------
    if OrderService.is_order_expired(order_id):
        return await message.answer(
            "⛔ **QR Code Expired**\n\n"
            "Please generate a new payment request.",
            reply_markup=premium_back_keyboard(),
            parse_mode="Markdown"
        )

    # ----------------------------------------------------
    # ORDER CONFIRMED BY ADMIN → Activate premium instantly
    # ----------------------------------------------------
    if order["status"] == "paid":
        await activate_premium_for_user(message, order)
        return

    # ----------------------------------------------------
    # ORDER STILL PENDING → Show "If you paid..." message
    # ----------------------------------------------------
    wait_msg = await message.answer(
        "⏳ Checking payment...\nThis may take 10–15 minutes...",
        parse_mode="Markdown"
    )

    # Delete after 3 seconds
    await asyncio.sleep(3)
    try:
        await wait_msg.delete()
    except:
        pass

    # Replace the message with the FINAL message
    await message.answer(
        "📨 **If you have paid, your order will be confirmed within 10 hours.**\n\n"
        f"🆔 Order ID: `{order_id}`",
        reply_markup=payment_verify_keyboard(order_id),
        parse_mode="Markdown"
    )



# ================================================================
# 3️⃣ PREMIUM ACTIVATION PROCESS
# ================================================================
async def activate_premium_for_user(message: types.Message, order: dict):
    """
    Called when order.status == 'paid'
    """

    user_id = order["user_id"]
    plan_id = order["plan_id"]

    plan = PlanService.get_plan(plan_id)
    if not plan:
        return await message.answer(
            "⚠ Plan no longer exists. Contact admin.",
            parse_mode="Markdown"
        )

    plan_days = plan["days"]
    expiry = PremiumService.activate_premium(user_id, plan_days, plan_id)

    # VERIFIED SUCCESSFUL MESSAGE
    await message.answer(
        "🎉 **PAYMENT VERIFIED! PREMIUM ACTIVATED**\n\n"
        f"💎 Plan: `{plan_days} days`\n"
        f"📅 Expires on: `{expiry}`\n\n"
        "Thank you for your purchase!",
        parse_mode="Markdown"
    )
