# bot_user/handlers/bypass_detection.py

from aiogram import Router, types
from aiogram.filters import CommandStart
from core.security.token_encryptor import decode_payload
from core.database import db
from bot_user.keyboards.inline_buttons import try_again_keyboard
from bot_user.handlers.force_sub_checker import check_force_sub

router = Router()


@router.message(CommandStart(deep_link_prefix="bypass_"))
async def bypass_detected(message: types.Message):
    """
    Triggered when redirect server sends deep-link:
    /start bypass_<token>

    This means:
    - User attempted to skip the shortlink
    - Verification failed
    """

    user_id = message.from_user.id
    data = message.text.replace("/start ", "")

    # Remove prefix
    token = data.replace("bypass_", "")  

    # Try decoding payload
    payload = decode_payload(token)
    if not payload:
        return await message.answer(
            "⚠ **Invalid or corrupted verification token.**",
            parse_mode="Markdown"
        )

    # Payload contains: post_no, file_id
    post_no = payload.get("post_no")
    file_id = payload.get("file_id")

    # ---------------------------------------
    # CHECK FORCE SUB FIRST
    # ---------------------------------------
    ok = await check_force_sub(message)
    if not ok:
        # Force-sub handler already sends the required UI
        return

    # ---------------------------------------
    # LOG THE BYPASS ATTEMPT
    # ---------------------------------------
    db.bypass.insert_one({
        "user_id": user_id,
        "token": token,
        "payload": payload,
        "file_id": file_id,
        "post_no": post_no
    })

    # ---------------------------------------
    # SHOW "BYPASS DETECTED" UI
    # (Your screenshot style)
    # ---------------------------------------
    text = (
        "⚠ **BY-PASS DETECTED!**\n\n"
        "›› It seems you tried to skip the verification link.\n"
        "›› You must complete verification to access this file.\n\n"
        "• Click **Try Again** below.\n"
    )

    await message.answer(
        text,
        reply_markup=try_again_keyboard(file_id, post_no),
        parse_mode="Markdown"
    )
