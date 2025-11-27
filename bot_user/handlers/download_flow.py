# bot_user/handlers/download_flow.py

from aiogram import Router, types
from aiogram.filters import CommandStart
from core.security.token_encryptor import decode_payload
from core.database import db
from core.utils.time_utils import now
from bot_user.handlers.force_sub_checker import check_force_sub
from bot_user.keyboards.inline_buttons import verify_keyboard, premium_offer_keyboard
from bot_user.keyboards.inline_buttons import clickhere_keyboard
from datetime import timedelta

router = Router()


@router.message(CommandStart(deep_link_prefix="get_"))
async def start_download(message: types.Message):
    """
    DOWNLOAD FLOW:
    --------------
    Triggered when user taps DOWNLOAD button in public group template.

    Deep-link example:
    /start get_<ENCODED_TOKEN>
    """

    user_id = message.from_user.id

    # -----------------------------------------
    # EXTRACT PAYLOAD
    # -----------------------------------------
    encoded = message.text.replace("/start ", "").replace("get_", "")
    payload = decode_payload(encoded)

    if not payload:
        return await message.answer(
            "⚠ **Invalid or corrupted link.**",
            parse_mode="Markdown"
        )

    file_id = payload.get("file_id")
    post_no = payload.get("post_no")

    if not file_id:
        return await message.answer(
            "⚠ **Invalid file request.**",
            parse_mode="Markdown"
        )

    # -----------------------------------------
    # FORCE SUBSCRIBE CHECK
    # -----------------------------------------
    is_ok = await check_force_sub(message)
    if not is_ok:
        return  # force-sub handler already sent UI

    # -----------------------------------------
    # CHECK USER STATUS (PREMIUM OR VERIFIED)
    # -----------------------------------------
    user = db.users.find_one({"user_id": user_id})
    current = now()

    premium_active = False
    verified_active = False

    if user:
        # PREMIUM CHECK
        if user.get("is_premium") and user.get("premium_expiry"):
            if user["premium_expiry"] > current:
                premium_active = True

        # VERIFICATION CHECK
        if user.get("is_verified") and user.get("verified_until"):
            if user["verified_until"] > current:
                verified_active = True

    # USER IS VERIFIED → deliver file directly
    if premium_active or verified_active:
        return await deliver_file(message, file_id, post_no)

    # -----------------------------------------
    # USER NOT VERIFIED → SHOW VERIFICATION SCREEN
    # EXACT TEMPLATE BASED ON YOUR SCREENSHOTS
    # -----------------------------------------
    text = (
        f"⚡ HEY, {message.from_user.first_name} ×~\n\n"
        "›› YOU NEED TO VERIFY A TOKEN TO GET FREE ACCESS FOR 1 DAY ✅\n\n"
        "›› IF YOU DONT WANT TO OPEN SHORT LINKS THEN YOU CAN TAKE PREMIUM SERVICES\n\n"
        "• VERIFY NOW •\n"
        "• GET PREMIUM (UNLIMITED) •\n"
        "• HOW TO VERIFY •"
    )

    await message.answer(
        text,
        reply_markup=verify_keyboard(encoded),
        parse_mode="Markdown"
    )


# ================================================================
# FILE DELIVERY LOGIC (AUTO-DELETE + CLICK HERE SYSTEM)
# ================================================================
async def deliver_file(message: types.Message, file_id: str, post_no: int):
    """
    Deliver file + auto-delete after X minutes.
    Also sends the CLICK-HERE flow.
    """

    user_id = message.from_user.id

    # -----------------------------------------
    # SEND FILE (message 1)
    # Caption includes PASSWORD as per your design
    # -----------------------------------------
    sent1 = await message.answer_document(
        file_id,
        caption="password - Legalstuff321"
    )

    # -----------------------------------------
    # Send a second duplicate file message (your screenshot behavior)
    # -----------------------------------------
    sent2 = await message.answer_document(
        file_id,
        caption="password - Legalstuff321"
    )

    # -----------------------------------------
    # AUTO DELETE TIME (can be configured)
    # Default: 5 minutes
    # -----------------------------------------
    delete_after_min = 5
    delete_after = timedelta(minutes=delete_after_min)

    # Store messages for cleanup system (CRON)
    db.temp_delivery.insert_one({
        "user_id": user_id,
        "file_id": file_id,
        "post_no": post_no,
        "msg1_id": sent1.message_id,
        "msg2_id": sent2.message_id,
        "chat_id": sent1.chat.id,
        "delete_after": now() + delete_after
    })

    # -----------------------------------------
    # SEND "CLICK HERE" INFO BLOCK (message 3)
    # -----------------------------------------
    await message.answer(
        f"✔ Your file for **Post - {post_no}** is delivered.\n"
        "Click below to get it again before expiry.",
        reply_markup=clickhere_keyboard(file_id),
        parse_mode="Markdown"
    )
