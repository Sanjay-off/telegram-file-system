# bot_admin/handlers/stats.py

from aiogram import Router, types
from aiogram.filters import Command
from bot_admin.utils.helpers import is_admin
from core.database import db
from core.utils.time_utils import now

router = Router()


# ---------------------------------------------------
# /users  → total registered users
# ---------------------------------------------------
@router.message(Command("users"))
async def total_users(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    count = db.users.count_documents({})
    await message.reply(f"👥 **Total Users:** `{count}`", parse_mode="Markdown")


# ---------------------------------------------------
# /verified → users with active shortlink verification
# ---------------------------------------------------
@router.message(Command("verified"))
async def verified_users(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    current_time = now()

    count = db.users.count_documents({
        "is_verified": True,
        "verified_until": {"$gt": current_time}
    })

    await message.reply(
        f"✔ **Active Verified Users:** `{count}`",
        parse_mode="Markdown"
    )


# ---------------------------------------------------
# /premiumusers → active premium users
# ---------------------------------------------------
@router.message(Command("premiumusers"))
async def premium_users(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    current_time = now()

    count = db.users.count_documents({
        "is_premium": True,
        "premium_expiry": {"$gt": current_time}
    })

    await message.reply(
        f"💎 **Active Premium Users:** `{count}`",
        parse_mode="Markdown"
    )


# ---------------------------------------------------
# /stats → full detailed bot statistics
# ---------------------------------------------------
@router.message(Command("stats"))
async def full_stats(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    current_time = now()

    total_users = db.users.count_documents({})
    verified = db.users.count_documents({
        "is_verified": True,
        "verified_until": {"$gt": current_time}
    })
    premium = db.users.count_documents({
        "is_premium": True,
        "premium_expiry": {"$gt": current_time}
    })
    pending_orders = db.orders.count_documents({"status": "pending"})
    expired_orders = db.orders.count_documents({"status": "expired"})
    total_orders = db.orders.count_documents({})
    
    text = (
        "📊 **Bot Statistics**\n\n"
        f"👥 **Total Users:** `{total_users}`\n"
        f"✔ **Active Verified Users:** `{verified}`\n"
        f"💎 **Active Premium Users:** `{premium}`\n\n"
        f"📦 **Orders Summary:**\n"
        f"— Pending: `{pending_orders}`\n"
        f"— Expired: `{expired_orders}`\n"
        f"— Total Orders: `{total_orders}`\n"
    )

    await message.reply(text, parse_mode="Markdown")
