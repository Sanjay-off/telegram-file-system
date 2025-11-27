# bot_user/handlers/start.py

from aiogram import Router, types
from aiogram.filters import CommandStart
from core.database import db
from core.utils.time_utils import now

router = Router()


@router.message(CommandStart(deep_link=False))
async def user_start(message: types.Message):
    """
    Handles /start when NO deep-link payload is present.
    (Normal start of the bot)
    """

    user_id = message.from_user.id
    first_name = message.from_user.first_name
    current = now()

    # -----------------------------------------
    # REGISTER USER IF NOT EXISTS
    # -----------------------------------------
    user = db.users.find_one({"user_id": user_id})
    if not user:
        db.users.insert_one({
            "user_id": user_id,
            "joined_at": current,
            "is_verified": False,
            "verified_until": None,
            "is_premium": False,
            "premium_expiry": None
        })

    # -----------------------------------------
    # DETERMINE USER STATUS
    # -----------------------------------------
    status = "🟥 Not Verified"

    if user:
        # Premium
        if user.get("is_premium") and user.get("premium_expiry", current) > current:
            status = "💎 Premium User"
        # Verified
        elif user.get("is_verified") and user.get("verified_until", current) > current:
            status = "🟦 Verified User"

    # -----------------------------------------
    # WELCOME MESSAGE (CLEAN UI)
    # -----------------------------------------
    text = (
        f"👋 **Hello, {first_name}!**\n\n"
        f"Your Status: {status}\n\n"
        "Welcome to the File Delivery Bot.\n"
        "You will receive files after completing verification or using premium.\n\n"
        "**Available Commands:**\n"
        "• `/start` — Restart the bot\n"
        "• `/help` — Show help guide\n"
        "• `/checkpremium` — Check premium validity\n"
        "• `/id` — Show your Telegram ID\n\n"
        "To download a file, click a **DOWNLOAD** button from a public post."
    )

    await message.answer(text, parse_mode="Markdown")
