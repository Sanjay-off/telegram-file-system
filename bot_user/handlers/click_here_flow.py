# bot_user/handlers/click_here_flow.py

from aiogram import Router, types
from aiogram.filters import CommandStart
from core.security.token_encryptor import decode_payload
from core.database import db
from bot_user.handlers.force_sub_checker import check_force_sub
from bot_user.keyboards.inline_buttons import clickhere_keyboard, close_message_keyboard

router = Router()

"""
CLICK HERE FLOW:
----------------
Triggered after files are auto-deleted.

Deep link: /start click_<ENCODED>

Steps:
1. Decode payload (file_id, post_no)
2. Check force-sub
3. Check premium OR verification status
4. Show "Click Here" template (matching your screenshot)
"""

@router.message(CommandStart(deep_link_prefix="click_"))
async def click_here_handler(message: types.Message):
    user_id = message.from_user.id

    # Extract encoded payload
    data = message.text.replace("/start ", "")
    encoded = data.replace("click_", "")

    payload = decode_payload(encoded)
    if not payload:
        return await message.answer(
            "⚠ **Invalid or corrupted link.**",
            parse_mode="Markdown"
        )

    file_id = payload.get("file_id")
    post_no = payload.get("post_no")

    # -----------------------------------------
    # FORCE SUB CHECK
    # -----------------------------------------
    ok = await check_force_sub(message)
    if not ok:
        return

    # -----------------------------------------
    # CHECK IF USER IS VERIFIED OR PREMIUM
    # -----------------------------------------
    user = db.users.find_one({"user_id": user_id})
    valid_verified = False

    if user:
        # Premium overrides everything
        if user.get("is_premium") and user.get("premium_expiry"):
            if user["premium_expiry"] > message.date:
                valid_verified = True

        # Verification check
        if user.get("is_verified") and user.get("verified_until"):
            if user["verified_until"] > message.date:
                valid_verified = True

    if not valid_verified:
        return await message.answer(
            "⚠ **Your verification has expired.**\n"
            "Please verify again to access this file.",
            parse_mode="Markdown"
        )

    # -----------------------------------------
    # SEND THE "CLICK HERE" FLOW UI
    # (Matches your screenshot exactly)
    # -----------------------------------------

    # 1️⃣ Send the “INFO” block
    await message.answer(
        "✔️ Your file download window is active.\n\n"
        "You can click below to get your file again.",
        reply_markup=close_message_keyboard(),
        parse_mode="Markdown"
    )

    # 2️⃣ Send the CLICK HERE button block
    await message.answer(
        f"📦 **Post - {post_no}**\n\n"
        "Click the button below to download your file again.",
        reply_markup=clickhere_keyboard(encoded),
        parse_mode="Markdown"
    )
