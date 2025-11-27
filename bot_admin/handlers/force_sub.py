# bot_admin/handlers/force_sub.py

from aiogram import Router, types
from aiogram.filters import Command
from bot_admin.utils.helpers import is_admin
from core.database import db

router = Router()


# ---------------------------------------------------
# ADD FORCE-SUB CHANNEL
# ---------------------------------------------------
@router.message(Command("addforce"))
async def add_force_sub(message: types.Message):
    """
    Usage:
        /addforce @channelname ButtonText
    """
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split(maxsplit=2)

    if len(parts) < 3:
        return await message.reply(
            "⚠ Usage:\n"
            "`/addforce @channelname ButtonText`",
            parse_mode="Markdown"
        )

    channel_username = parts[1].strip()
    button_text = parts[2].strip()

    if not channel_username.startswith("@"):
        return await message.reply("❌ Channel must start with @")

    entry = {
        "channel": channel_username,
        "button_text": button_text
    }

    db.settings.update_one(
        {"key": "force_sub"},
        {"$addToSet": {"value": entry}},
        upsert=True
    )

    await message.reply(
        f"✅ **Force-sub channel added**\n\n"
        f"📢 Channel: `{channel_username}`\n"
        f"🔘 Button Text: `{button_text}`",
        parse_mode="Markdown"
    )


# ---------------------------------------------------
# REMOVE FORCE-SUB CHANNEL
# ---------------------------------------------------
@router.message(Command("removeforce"))
async def remove_force_sub(message: types.Message):
    """
    Usage:
        /removeforce @channelname
    """
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply(
            "⚠ Usage:\n"
            "`/removeforce @channelname`",
            parse_mode="Markdown"
        )

    channel_username = parts[1]

    db.settings.update_one(
        {"key": "force_sub"},
        {"$pull": {"value": {"channel": channel_username}}}
    )

    await message.reply(
        f"🗑 Removed force-sub channel: `{channel_username}`",
        parse_mode="Markdown"
    )


# ---------------------------------------------------
# LIST FORCE-SUB CHANNELS
# ---------------------------------------------------
@router.message(Command("listforce"))
async def list_force_sub(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    doc = db.settings.find_one({"key": "force_sub"})
    channels = doc["value"] if doc else []

    if not channels:
        return await message.reply("⚠ No force-sub channels added yet.")

    text = "📢 **Force-Subscribe Channels:**\n\n"

    for i, ch in enumerate(channels, 1):
        text += f"**{i}.** `{ch['channel']}` → Button: *{ch['button_text']}*\n"

    await message.reply(text, parse_mode="Markdown")

