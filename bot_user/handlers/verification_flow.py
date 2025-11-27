# bot_user/handlers/verification_flow.py

from aiogram import Router, types
from aiogram.filters import CommandStart
from core.database import db
from core.security.token_encryptor import encode_payload, decode_payload
from core.utils.time_utils import now
from bot_user.handlers.force_sub_checker import check_force_sub
from bot_admin.services.shortener_service import ShortenerService
from bot_user.keyboards.inline_buttons import (
    verify_now_button,
    get_premium_button,
    how_to_verify_button,
    verification_main_keyboard,
)
from datetime import timedelta

router = Router()


# ===================================================================
# STEP 1 — USER CLICKS "VERIFY NOW"
# deep-link prefix: verify_<encoded>
# ===================================================================
@router.message(CommandStart(deep_link_prefix="verify_"))
async def verification_start_handler(message: types.Message):
    """
    User tapped "VERIFY NOW" from the verify panel.
    The bot must:
    - Decode the payload
    - Check force-sub
    - Generate shortlink
    - Send them to the redirect link
    """

    user_id = message.from_user.id

    # Extract encoded payload
    raw = message.text.replace("/start ", "")
    encoded = raw.replace("verify_", "")

    payload = decode_payload(encoded)
    if not payload:
        return await invalid_token(message)

    # File information (optional, but stored)
    file_id = payload.get("file_id")
    post_no = payload.get("post_no")

    # Step 1 — Force-Sub Check
    ok = await check_force_sub(message)
    if not ok:
        return

    # Step 2 — Create verification token (for redirect server)
    verify_token = encode_payload({
        "user_id": user_id,
        "file_id": file_id,
        "post_no": post_no
    })

    # Build redirect link
    redirect_url = f"{db.settings.find_one({'key':'redirect_base'})['value']}?token={verify_token}"

    # Step 3 — Choose a shortener
    selected = ShortenerService.get_random()
    if not selected:
        # No shortener configured → send redirect directly
        short_url = redirect_url
    else:
        short_url = build_shortened_link(selected, redirect_url)

    # Step 4 — Show verification instruction
    await message.answer(
        "🔗 **TOKEN VERIFICATION REQUIRED**\n\n"
        "Click the button below to begin verification.\n\n"
        "After completing, you will be redirected back to this bot.",
        reply_markup=verification_main_keyboard(short_url, encoded),
        parse_mode="Markdown"
    )


# ===================================================================
# STEP 2 — USER RETURNS SUCCESSFULLY FROM REDIRECT SERVER
# deep-link prefix: verified_<token>
# ===================================================================
@router.message(CommandStart(deep_link_prefix="verified_"))
async def verified_success_handler(message: types.Message):
    """
    Token was validated by redirect server.
    User did NOT bypass.
    Must:
    - Mark user as verified
    - Add verification duration
    - Send "VERIFIED SUCCESSFULLY" as a NEW MESSAGE
    """

    raw = message.text.replace("/start ", "")
    encoded = raw.replace("verified_", "")

    payload = decode_payload(encoded)
    if not payload:
        return await invalid_token(message)

    user_id = payload.get("user_id")
    file_id = payload.get("file_id")
    post_no = payload.get("post_no")

    # Free access duration
    doc = db.settings.find_one({"key": "free_access_hours"})
    free_hours = doc["value"] if doc else 1

    expiry = now() + timedelta(hours=free_hours)

    # Update user DB
    db.users.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "is_verified": True,
                "verified_until": expiry
            }
        },
        upsert=True
    )

    # Send success message as a NEW MESSAGE
    await message.answer(
        "🎉 **VERIFIED SUCCESSFULLY!**\n\n"
        f"Your verification is valid for `{free_hours}` hours.",
        parse_mode="Markdown"
    )

    # Optional: auto-deliver file
    if file_id and post_no:
        from bot_user.handlers.file_delivery import deliver_file_core
        await deliver_file_core(message, file_id, post_no)


# ===================================================================
# INVALID TOKEN (Screenshot 2)
# ===================================================================
async def invalid_token(message: types.Message):
    return await message.answer(
        "❌ **INVALID / EXPIRED VERIFICATION TOKEN**\n\n"
        "Please try verifying again.",
        parse_mode="Markdown"
    )


# ===================================================================
# SHORTENING API CALLER
# ===================================================================
def build_shortened_link(shortener, redirect_url):
    """
    Dummy shortener builder.
    Real implementation:
    GET https://domain/api?api=API_KEY&url=...
    """
    domain = shortener["domain"]
    api = shortener["api_key"]

    # In production, you'd do an HTTP request to the shortener.
    # Here we emulate the behavior by constructing a fake shortened URL.
    # Your redirect server will catch real verification.
    return f"https://{domain}/api?api={api}&url={redirect_url}"
