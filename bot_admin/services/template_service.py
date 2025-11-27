# bot_admin/services/template_service.py

from core.database import db
from core.security.token_encryptor import encode_payload
from core.config import config
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class TemplateService:

    # ---------------------------------------------------
    # GET FILE DATA
    # ---------------------------------------------------
    @staticmethod
    def get_file(file_db_id: str):
        """
        Return file document from DB.
        """
        return db.files.find_one({"file_db_id": file_db_id})

    # ---------------------------------------------------
    # BUILD TEMPLATE TEXT + KEYBOARD
    # ---------------------------------------------------
    @staticmethod
    def generate_template(file_data: dict):
        """
        Takes the file metadata and generates:
        - Template text (Post - X ...)
        - Inline keyboard download button
        """

        post_no = file_data["post_no"]
        description = file_data["description"]
        extra = file_data["extra_message"]
        file_id = file_data["file_id"]

        # ----------------------------------------------
        # SECURE ENCODED PAYLOAD
        # ----------------------------------------------
        payload = {
            "action": "get",
            "file_id": file_id,
            "post_no": post_no
        }

        encoded = encode_payload(payload)
        bot_username = config.BOT_B_USERNAME
        final_link = f"https://t.me/{bot_username}?start={encoded}"

        # ----------------------------------------------
        # TEXT TEMPLATE (EXACT FORMAT YOU REQUESTED)
        # ----------------------------------------------
        text = (
            f"Post - {post_no}\n\n"
            f"> {description}\n\n"
            f"> {extra}"
        )

        # ----------------------------------------------
        # INLINE KEYBOARD
        # ----------------------------------------------
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⬇️ DOWNLOAD ⬇️",
                        url=final_link
                    )
                ]
            ]
        )

        return text, keyboard

    # ---------------------------------------------------
    # FULL API → Generate FULL Template from DB ID
    # ---------------------------------------------------
    @staticmethod
    def generate_by_id(file_db_id: str):
        """
        High-level function:
        1. Fetch file
        2. Generate template text + keyboard
        """

        file_data = TemplateService.get_file(file_db_id)
        if not file_data:
            return None, None  # file not found

        return TemplateService.generate_template(file_data)
