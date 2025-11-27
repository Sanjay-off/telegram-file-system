# bot_admin/handlers/shortener_settings.py

from aiogram import Router, types
from aiogram.filters import Command
from bot_admin.utils.helpers import is_admin
from core.database import db

router = Router()


# ---------------------------------------------------
# /addshortener <domain> <api_key>
# Example:
# /addshortener get2short.com APIKEY123
# ---------------------------------------------------
@router.message(Command("addshortener"))
async def add_shortener(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split(maxsplit=2)

    if len(parts) < 3:
        return await message.reply(
            "⚠ Usage:\n"
            "`/addshortener <domain> <api_key>`\n\n"
            "Example:\n"
            "`/addshortener get2short.com API_KEY_12345`",
            parse_mode="Markdown"
        )

    domain = parts[1].strip().lower()
    api_key = parts[2].strip()

    entry = {
        "domain": domain,
        "api_key": api_key
    }

    db.settings.update_one(
        {"key": "shorteners"},
        {"$addToSet": {"value": entry}},
        upsert=True
    )

    await message.reply(
        f"✅ **Shortener Added**\n\n"
        f"🔗 Domain: `{domain}`\n"
        f"🔑 API Key: `{api_key}`",
        parse_mode="Markdown"
    )


# ---------------------------------------------------
# /removeshortener <domain>
# ---------------------------------------------------
@router.message(Command("removeshortener"))
async def remove_shortener(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply(
            "⚠ Usage:\n"
            "`/removeshortener <domain>`\n\n"
            "Example:\n"
            "`/removeshortener get2short.com`",
            parse_mode="Markdown"
        )

    domain = parts[1].strip().lower()

    db.settings.update_one(
        {"key": "shorteners"},
        {"$pull": {"value": {"domain": domain}}},
    )

    await message.reply(
        f"🗑 **Shortener Removed:** `{domain}`",
        parse_mode="Markdown"
    )


# ---------------------------------------------------
# /listshorteners
# ---------------------------------------------------
@router.message(Command("listshorteners"))
async def list_shorteners(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    doc = db.settings.find_one({"key": "shorteners"})
    items = doc["value"] if doc else []

    if not items:
        return await message.reply("⚠ No shortener platforms added yet.")

    text = "🔗 **Shortener Platforms:**\n\n"

    for i, s in enumerate(items, 1):
        text += (
            f"**{i}.** `{s['domain']}`\n"
            f"🔑 API Key: `{s['api_key']}`\n"
            "--------------------------\n"
        )

    await message.reply(text, parse_mode="Markdown")
