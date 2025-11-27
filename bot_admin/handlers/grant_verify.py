# bot_admin/handlers/grant_verify.py

from aiogram import Router, types
from aiogram.filters import Command
from bot_admin.utils.helpers import is_admin
from core.database import db
from datetime import datetime, timedelta
from core.utils.time_utils import now

router = Router()


# ---------------------------------------------------
# /grantverify <user_id> <hours>
# Manually verify a user for X hours (free access)
# ---------------------------------------------------
@router.message(Command("grantverify"))
async def grant_manual_verification(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split()

    if len(parts) < 3:
        return await message.reply(
            "⚠ Usage:\n"
            "`/grantverify <user_id> <hours>`",
            parse_mode="Markdown"
        )

    # -----------------------
    # Validate user_id
    # -----------------------
    try:
        user_id = int(parts[1])
    except:
        return await message.reply("❌ Invalid user ID.")

    # -----------------------
    # Validate hours
    # -----------------------
    try:
        hours = int(parts[2])
        if hours <= 0:
            return await message.reply("❌ Hours must be greater than 0.")
    except:
        return await message.reply("❌ Hours must be a valid number.")

    # -----------------------
    # Calculate expiry
    # -----------------------
    expiry_time = now() + timedelta(hours=hours)

    # Upsert user record
    db.users.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "manual_verified_until": expiry_time,
                "is_verified": True,
            }
        },
        upsert=True
    )

    await message.reply(
        f"✅ **User Manually Verified!**\n\n"
        f"👤 User: `{user_id}`\n"
        f"⏳ Valid for: `{hours}` hours\n"
        f"📅 Expires at: `{expiry_time}`",
        parse_mode="Markdown"
    )

    # ---------------------------------------------------
    # Notify user (optional if they didn't block bot)
    # ---------------------------------------------------
    try:
        await message.bot.send_message(
            user_id,
            f"🎉 You have been manually verified by admin!\n\n"
            f"⏳ Valid for **{hours} hours**.\n"
            f"Enjoy instant file access!",
            parse_mode="Markdown"
        )
    except:
        pass
