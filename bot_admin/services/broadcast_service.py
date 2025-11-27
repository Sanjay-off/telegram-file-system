# bot_admin/services/broadcast_service.py

import asyncio
from core.database import db
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest


class BroadcastService:

    @staticmethod
    async def send_text(bot, text: str):
        """
        Broadcast plain text message to all users.
        """
        return await BroadcastService._broadcast(bot, text=text, mode="text")

    @staticmethod
    async def send_photo(bot, photo_file_id: str, caption: str = ""):
        """
        Broadcast photo with caption.
        """
        return await BroadcastService._broadcast(bot, file_id=photo_file_id, text=caption, mode="photo")

    @staticmethod
    async def send_document(bot, file_id: str, caption: str = ""):
        """
        Broadcast document or video with caption.
        """
        return await BroadcastService._broadcast(bot, file_id=file_id, text=caption, mode="file")

    # ----------------------------------------------------------
    # INTERNAL BROADCAST FUNCTION
    # ----------------------------------------------------------
    @staticmethod
    async def _broadcast(bot, text: str = "", file_id: str = None, mode: str = "text"):
        """
        Core broadcast logic.
        Sends to all users with safe rate-limiting (1 msg/sec).
        """

        users = db.users.find({}, {"user_id": 1})

        total = 0
        success = 0
        failed = 0

        async def send_message(uid):
            nonlocal success, failed

            try:
                if mode == "text":
                    await bot.send_message(uid, text)
                elif mode == "photo":
                    await bot.send_photo(uid, file_id, caption=text)
                elif mode == "file":
                    await bot.send_document(uid, file_id, caption=text)

                success += 1

            except (TelegramForbiddenError, TelegramBadRequest):
                failed += 1

        # Send 1 message per second to avoid flood limits
        for user in users:
            uid = user["user_id"]
            total += 1

            await send_message(uid)
            await asyncio.sleep(1)

        return {
            "total": total,
            "success": success,
            "failed": failed
        }
