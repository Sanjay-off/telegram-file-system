# bot_user/utils/helpers.py

import asyncio
from aiogram import types
from core.database import db
from core.utils.time_utils import now


class UserHelpers:

    # ---------------------------------------------------------
    # REGISTER USER IF FIRST TIME
    # ---------------------------------------------------------
    @staticmethod
    def register_user_if_needed(user_id: int):
        """
        Creates a new DB user if not exists.
        """
        if not db.users.find_one({"user_id": user_id}):
            db.users.insert_one({
                "user_id": user_id,
                "joined_at": now(),
                "is_verified": False,
                "verified_until": None,
                "is_premium": False,
                "premium_expiry": None
            })
        return True

    # ---------------------------------------------------------
    # FORMAT USERNAME / FIRST NAME
    # ---------------------------------------------------------
    @staticmethod
    def username_safe(user: types.User) -> str:
        """
        Returns @username if available else first name.
        """
        if user.username:
            return f"@{user.username}"
        return user.first_name or "User"

    # ---------------------------------------------------------
    # CLEAN MARKDOWN SPECIAL CHARACTERS
    # ---------------------------------------------------------
    @staticmethod
    def md_escape(text: str) -> str:
        """
        Escapes characters that break Markdown formatting.
        """
        if not text:
            return ""
        for ch in ("_", "*", "[", "]", "(", ")", "~", "`", ">", "#", "+", "-", "=", "|", "{", "}", ".", "!"):
            text = text.replace(ch, f"\\{ch}")
        return text

    # ---------------------------------------------------------
    # DELETE A MESSAGE SAFELY
    # ---------------------------------------------------------
    @staticmethod
    async def safe_delete_message(message: types.Message):
        """
        Deletes a message but ignores Telegram errors.
        """
        try:
            await message.delete()
        except:
            pass

    # ---------------------------------------------------------
    # SEND TEMPORARY MESSAGE (AUTO-DELETE)
    # ---------------------------------------------------------
    @staticmethod
    async def temp_message(chat: types.Message, text: str, delay: float = 3.0):
        """
        Sends a temporary message that auto-deletes after `delay` seconds.
        """
        msg = await chat.answer(text, parse_mode="Markdown")
        await asyncio.sleep(delay)
        try:
            await msg.delete()
        except:
            pass
        return True

    # ---------------------------------------------------------
    # GET USER STATUS (PREMIUM / VERIFIED / NORMAL)
    # ---------------------------------------------------------
    @staticmethod
    def get_user_status(user_id: int) -> str:
        user = db.users.find_one({"user_id": user_id})
        current = now()

        if not user:
            return "normal"

        # Premium
        if user.get("is_premium") and user.get("premium_expiry", current) > current:
            return "premium"

        # Verified
        if user.get("is_verified") and user.get("verified_until", current) > current:
            return "verified"

        return "normal"

    # ---------------------------------------------------------
    # EXTRACT DEEPLINK PAYLOAD SAFELY
    # ---------------------------------------------------------
    @staticmethod
    def get_deeplink_data(message: types.Message) -> str:
        """
        Returns the deep-link argument safely:
        /start abcdef → "abcdef"
        /start xyz?param=1 → "xyz?param=1"
        """
        if not message.text.startswith("/start"):
            return ""

        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            return ""
        return parts[1].strip()

    # ---------------------------------------------------------
    # SMALL ASYNC DELAY (avoid spamming Telegram)
    # ---------------------------------------------------------
    @staticmethod
    async def cooldown(sec: float = 0.3):
        await asyncio.sleep(sec)
