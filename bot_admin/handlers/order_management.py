# bot_admin/handlers/order_management.py

from aiogram import Router, types
from aiogram.filters import Command
from bot_admin.utils.helpers import is_admin
from core.database import db
from core.utils.time_utils import now
from datetime import timedelta

router = Router()


# ---------------------------------------------------
# /orders  (all)
# /orders pending
# /orders expired
# ---------------------------------------------------
@router.message(Command("orders"))
async def list_orders(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split()
    filter_type = parts[1] if len(parts) > 1 else "all"

    query = {}

    if filter_type == "pending":
        query = {"status": "pending"}
    elif filter_type == "expired":
        query = {"status": "expired"}
    else:
        query = {}  # show all

    orders = list(db.orders.find(query).sort("created_at", -1).limit(30))

    if not orders:
        return await message.reply("⚠ No orders found.")

    text = f"📦 **Orders — {filter_type.upper()}**\n\n"

    for o in orders:
        text += (
            f"🆔 `{o['order_id']}`\n"
            f"👤 User: `{o['user_id']}`\n"
            f"💰 Amount: ₹{o['amount']}\n"
            f"🗓 Created: `{o['created_at']}`\n"
            f"📌 Status: `{o['status']}`\n\n"
        )

    await message.reply(text, parse_mode="Markdown")


# ---------------------------------------------------
# /order <order_id> → view details
# ---------------------------------------------------
@router.message(Command("order"))
async def view_order(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply("⚠ Usage: /order <order_id>")

    order_id = parts[1]

    order = db.orders.find_one({"order_id": order_id})
    if not order:
        return await message.reply("❌ Order not found.")

    text = (
        f"🆔 **Order ID:** `{order['order_id']}`\n"
        f"👤 **User:** `{order['user_id']}`\n"
        f"💎 **Plan ID:** `{order['plan_id']}`\n"
        f"💰 **Amount:** ₹{order['amount']}\n"
        f"⏳ **Status:** `{order['status']}`\n"
        f"🗓 **Created:** `{order['created_at']}`\n"
        f"⌛ **Expires:** `{order['expires_at']}`\n"
        f"🔁 **Confirm Window Until:** `{order['confirm_until']}`"
    )

    await message.reply(text, parse_mode="Markdown")


# ---------------------------------------------------
# /confirmorder <order_id>  → set as paid
# ---------------------------------------------------
@router.message(Command("confirmorder"))
async def confirm_order(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply("⚠ Usage: /confirmorder <order_id>")

    order_id = parts[1]

    order = db.orders.find_one({"order_id": order_id})
    if not order:
        return await message.reply("❌ Order not found.")

    if order["status"] == "paid":
        return await message.reply("ℹ This order is already marked as PAID.")

    # Check confirm window (10 hours)
    if now() > order["confirm_until"]:
        return await message.reply("❌ Cannot confirm. Order confirm window expired.")

    # ------------------------------------------------
    # UPDATE ORDER STATUS
    # ------------------------------------------------
    db.orders.update_one(
        {"order_id": order_id},
        {"$set": {"status": "paid", "paid_at": now()}}
    )

    # ------------------------------------------------
    # ACTIVATE PREMIUM
    # ------------------------------------------------
    user_id = order["user_id"]
    plan_id = order["plan_id"]

    plan = db.plans.find_one({"plan_id": plan_id})
    if not plan:
        return await message.reply("❌ Plan linked to this order no longer exists.")

    plan_days = plan.get("days", 0)

    user = db.users.find_one({"user_id": user_id})

    # Premium stacking logic
    if user and "premium_expiry" in user and user["premium_expiry"] > now():
        # User already has premium → extend
        new_expiry = user["premium_expiry"] + timedelta(days=plan_days)
    else:
        # New premium
        new_expiry = now() + timedelta(days=plan_days)

    # Update user premium status
    db.users.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "is_premium": True,
                "premium_expiry": new_expiry,
                "premium_plan": plan_id,
            }
        },
        upsert=True
    )

    await message.reply(
        f"✅ Order `{order_id}` confirmed.\n"
        f"👤 User `{user_id}` premium activated.\n"
        f"⏳ Expires: `{new_expiry}`",
        parse_mode="Markdown"
    )

    # Notify user (if bot not blocked)
    try:
        await message.bot.send_message(
            user_id,
            f"🎉 **Your payment was confirmed!**\n\n"
            f"💎 Premium Activated\n"
            f"🕒 Valid for: `{plan_days}` days\n"
            f"📅 Expires on: `{new_expiry}`",
            parse_mode="Markdown"
        )
    except:
        pass


# ---------------------------------------------------
# /refundorder <order_id>
# (optional, does NOT remove premium)
# ---------------------------------------------------
@router.message(Command("refundorder"))
async def refund_order(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply("⚠ Usage: /refundorder <order_id>")

    order_id = parts[1]

    order = db.orders.find_one({"order_id": order_id})
    if not order:
        return await message.reply("❌ Order not found.")

    db.orders.update_one(
        {"order_id": order_id},
        {"$set": {"status": "refunded"}}
    )

    await message.reply(f"💸 Order `{order_id}` marked as REFUNDED.", parse_mode="Markdown")
