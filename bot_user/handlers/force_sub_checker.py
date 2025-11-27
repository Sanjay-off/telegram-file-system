# bot_user/handlers/force_sub_checker.py

from aiogram import Router, types
from aiogram.exceptions import TelegramBadRequest
from core.database import db
from bot_user.keyboards.inline_buttons import force_sub_keyboard

router = Router()


async def check_force_sub(message: types.Message) -> bool:
    """
    Returns True if the user is subscribed to ALL required channels.
    Else → sends Force-Sub UI and returns False.
    """

    user_id = message.from_user.id
    bot = message.bot

    # -----------------------------------------
    # FETCH FORCE-SUB LIST
    # -----------------------------------------
    doc = db.settings.find_one({"key": "force_sub"})
    channels = doc["value"] if doc else []

    # If no force-sub channels configured → allow access
    if not channels:
        return True

    not_joined = []

    # -----------------------------------------
    # CHECK SUBSCRIPTION STATUS
    # -----------------------------------------
    for ch in channels:
        channel_username = ch["channel"]

        try:
            member = await bot.get_chat_member(channel_username, user_id)

            if member.status in ["left", "kicked"]:
                not_joined.append(ch)

        except TelegramBadRequest:
            # Channel not found or bot not admin
            not_joined.append(ch)

    # -----------------------------------------
    # USER IS SUBSCRIBED TO ALL CHANNELS
    # -----------------------------------------
    if not not_joined:
        return True

    # -----------------------------------------
    # USER NOT SUBSCRIBED → SHOW FORCE SUB UI
    # EXACTLY LIKE YOUR SCREENSHOTS
    # -----------------------------------------
    await message.answer(
        "⚠ **You must join the required channels to continue.**\n\n"
        "👉 After joining, click **Try Again**.",
        reply_markup=force_sub_keyboard(not_joined),
        parse_mode="Markdown"
    )

    return False
