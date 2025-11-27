# bot_user/handlers/help.py

from aiogram import Router, types
from aiogram.filters import Command
from core.database import db
from core.utils.time_utils import now

router = Router()


@router.message(Command("help"))
async def user_help(message: types.Message):
    user_id = message.from_user.id
    user = db.users.find_one({"user_id": user_id})
    current = now()

    # Determine user status
    status_text = "🟥 Not Verified"
    if user:
        # Premium
        if user.get("is_premium") and user.get("premium_expiry", current) > current:
            status_text = "🟩 Premium User"
        # Verified
        elif user.get("is_verified") and user.get("verified_until", current) > current:
            status_text = "🟦 Verified User"

    text = (
        f"👋 **Hello, {message.from_user.first_name}!**\n\n"
        f"Your Status: {status_text}\n\n"
        "Here are the commands you can use:\n\n"
        "• `/start` — Start the bot or open a download link\n"
        "• `/checkpremium` — Check your premium status\n"
        "• `/help` — Show this help message\n"
        "• `/id` — Show your Telegram User ID\n\n"
        "If you need support, contact the admin through the bot's verification or premium screens."
    )

    await message.answer(text, parse_mode="Markdown")
