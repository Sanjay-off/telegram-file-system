# bot_admin/handlers/file_template.py

from aiogram import Router, types
from aiogram.filters import Command
from core.database import db
from bot_admin.utils.helpers import is_admin
from core.security.token_encryptor import encode_payload
from core.config import config

router = Router()


# ---------------------------------------------------
# Generate public template for group posting
# ---------------------------------------------------
@router.message(Command("gentemplate"))
async def generate_template(message: types.Message):
    """
    Usage:
        /gentemplate <file_id_in_db>

    This will create the formatted template:
        Post - X
        > description
        > extra message
        + Download button (encoded link)
    """
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split()

    if len(parts) < 2:
        return await message.reply("⚠ Usage: `/gentemplate <file_db_id>`", parse_mode="Markdown")

    file_db_id = parts[1]

    # Fetch file from DB
    file_data = db.files.find_one({"file_db_id": file_db_id})
    if not file_data:
        return await message.reply("❌ File not found in database.")

    post_no = file_data.get("post_no")
    description = file_data.get("description")
    extra = file_data.get("extra_message")
    stored_file_id = file_data.get("file_id")

    # Encode secure payload for download
    payload = {
        "action": "get",
        "file_id": stored_file_id,
        "post_no": post_no
    }

    encoded = encode_payload(payload)
    bot_username = config.BOT_B_USERNAME  # from .env
    final_link = f"https://t.me/{bot_username}?start={encoded}"

    # ---------------------------------------------
    # Format EXACT template as you required
    # ---------------------------------------------
    text = (
        f"Post - {post_no}\n\n"
        f"> {description}\n\n"
        f"> {extra}"
    )

    # Download button EXACT as your screenshot
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="⬇️ DOWNLOAD ⬇️",
                    url=final_link
                )
            ]
        ]
    )

    # Send template to admin only
    await message.reply(
        "✅ Template Generated Successfully!\n\n"
        "Copy the message below and paste it in your PUBLIC GROUP:\n\n"
        "-----------------------------------------",
        parse_mode="Markdown"
    )

    await message.answer(text, reply_markup=keyboard)


