# bot_admin/handlers/verification_settings.py

from aiogram import Router, types
from aiogram.filters import Command
from bot_admin.utils.helpers import is_admin
from core.database import db

router = Router()


# ---------------------------------------------------
# /setverifyguide <url>
# ---------------------------------------------------
@router.message(Command("setverifyguide"))
async def set_verify_guide(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply(
            "⚠ Usage:\n"
            "`/setverifyguide <url>`",
            parse_mode="Markdown"
        )

    url = parts[1].strip()

    db.settings.update_one(
        {"key": "verify_guide"},
        {"$set": {"value": url}},
        upsert=True
    )

    await message.reply(
        f"📘 **Verification Guide Updated**\n\n"
        f"🔗 New URL:\n`{url}`",
        parse_mode="Markdown"
    )


# ---------------------------------------------------
# /showverifyguide
# ---------------------------------------------------
@router.message(Command("showverifyguide"))
async def show_verify_guide(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    doc = db.settings.find_one({"key": "verify_guide"})
    url = doc["value"] if doc else None

    if not url:
        return await message.reply("⚠ No verification guide has been set yet.")

    await message.reply(
        f"📘 **Current Verification Guide:**\n\n🔗 `{url}`",
        parse_mode="Markdown"
    )


# ---------------------------------------------------
# /setfreeaccess <hours>
# free access time after verification (default = 0)
# ---------------------------------------------------
@router.message(Command("setfreeaccess"))
async def set_free_access(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split()

    if len(parts) < 2:
        return await message.reply(
            "⚠ Usage:\n"
            "`/setfreeaccess <hours>`",
            parse_mode="Markdown"
        )

    try:
        hours = int(parts[1])
        if hours < 0:
            return await message.reply("❌ Hours cannot be negative.")
    except:
        return await message.reply("❌ Hours must be a valid number.")

    db.settings.update_one(
        {"key": "free_access_hours"},
        {"$set": {"value": hours}},
        upsert=True
    )

    await message.reply(
        f"⏳ **Free Access Duration Updated**\n"
        f"Users will remain verified for `{hours}` hours.",
        parse_mode="Markdown"
    )
