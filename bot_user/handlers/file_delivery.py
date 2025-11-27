# bot_user/handlers/file_delivery.py

from aiogram import types
from core.utils.time_utils import now
from core.database import db
from datetime import timedelta
from bot_user.keyboards.inline_buttons import clickhere_keyboard


async def deliver_file_core(message: types.Message, file_id: str, post_no: int):
    """
    Deliver the file to the user exactly like your screenshot:

    1️⃣ Send two copies of the ZIP file with caption:
        "password - Legalstuff321"

    2️⃣ Store both messages in DB for auto-delete

    3️⃣ Send CLICK HERE UI so user can get file again later
    """

    user_id = message.from_user.id

    # ----------------------------------------------------
    # FIRST FILE MESSAGE
    # ----------------------------------------------------
    sent1 = await message.answer_document(
        file_id,
        caption="password - Legalstuff321"
    )

    # ----------------------------------------------------
    # SECOND FILE MESSAGE (duplicate, as in your screenshot)
    # ----------------------------------------------------
    sent2 = await message.answer_document(
        file_id,
        caption="password - Legalstuff321"
    )

    # ----------------------------------------------------
    # AUTO DELETE TIMER SETTING
    # ----------------------------------------------------
    delete_after_minutes = 5    # You can make this editable from admin bot later
    delete_time = now() + timedelta(minutes=delete_after_minutes)

    # ----------------------------------------------------
    # SAVE TO TEMP COLLECTION FOR BACKGROUND DELETER
    # ----------------------------------------------------
    db.temp_delivery.insert_one({
        "user_id": user_id,
        "file_id": file_id,
        "post_no": post_no,
        "chat_id": message.chat.id,
        "msg1_id": sent1.message_id,
        "msg2_id": sent2.message_id,
        "delete_after": delete_time
    })

    # ----------------------------------------------------
    # SEND THE CLICK HERE UI (Post-Download Message)
    # ----------------------------------------------------
    await message.answer(
        f"✔ **File for Post - {post_no} Delivered Successfully!**\n\n"
        "Your file will auto-delete soon. Click below if you want to re-download.",
        reply_markup=clickhere_keyboard(file_id, post_no),
        parse_mode="Markdown"
    )
