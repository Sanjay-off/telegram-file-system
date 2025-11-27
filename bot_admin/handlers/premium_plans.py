# bot_admin/handlers/premium_plans.py

from aiogram import Router, types
from aiogram.filters import Command
from bot_admin.utils.helpers import is_admin, generate_plan_id
from core.database import db

router = Router()


# ---------------------------------------------------
# /addplan <days> <price>
# ---------------------------------------------------
@router.message(Command("addplan"))
async def add_plan(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split()

    if len(parts) < 3:
        return await message.reply(
            "⚠ Usage:\n`/addplan <days> <price>`\n\n"
            "Example:\n`/addplan 30 120`",
            parse_mode="Markdown"
        )

    # Validate days
    try:
        days = int(parts[1])
        if days <= 0:
            return await message.reply("❌ Days must be greater than 0.")
    except:
        return await message.reply("❌ Invalid number of days.")

    # Validate price
    try:
        price = float(parts[2])
        if price <= 0:
            return await message.reply("❌ Price must be greater than 0.")
    except:
        return await message.reply("❌ Invalid price.")

    plan_id = generate_plan_id()

    plan = {
        "plan_id": plan_id,
        "days": days,
        "price": price
    }

    db.plans.insert_one(plan)

    await message.reply(
        f"✅ **Plan Added Successfully!**\n\n"
        f"🆔 Plan ID: `{plan_id}`\n"
        f"📅 Duration: `{days}` days\n"
        f"💰 Price: `₹{price}`",
        parse_mode="Markdown"
    )


# ---------------------------------------------------
# /removeplan <plan_id>
# ---------------------------------------------------
@router.message(Command("removeplan"))
async def remove_plan(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split()

    if len(parts) < 2:
        return await message.reply(
            "⚠ Usage:\n`/removeplan <plan_id>`",
            parse_mode="Markdown"
        )

    plan_id = parts[1]

    result = db.plans.delete_one({"plan_id": plan_id})

    if result.deleted_count == 0:
        return await message.reply("❌ No plan found with that ID.")

    await message.reply(
        f"🗑 **Plan Removed:** `{plan_id}`",
        parse_mode="Markdown"
    )


# ---------------------------------------------------
# /listplans
# ---------------------------------------------------
@router.message(Command("listplans"))
async def list_plans(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    plans = list(db.plans.find().sort("days", 1))

    if not plans:
        return await message.reply("⚠ No premium plans added yet.")

    text = "💎 **Premium Plans:**\n\n"

    for p in plans:
        text += (
            f"🆔 **{p['plan_id']}**\n"
            f"📅 Days: `{p['days']}`\n"
            f"💰 Price: `₹{p['price']}`\n"
            "--------------------------\n"
        )

    await message.reply(text, parse_mode="Markdown")
