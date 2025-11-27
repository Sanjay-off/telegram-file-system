# jobs/cleanup_files.py

"""
Cleanup Job: Auto-delete delivered files
----------------------------------------

This script deletes:
  - File message #1 (zip + caption)
  - File message #2 (duplicate zip message)
  - Post-download "CLICK HERE" message (optional)
based on temp_delivery.delete_after timestamp.

Structure of temp_delivery:
{
  "user_id": 123,
  "file_id": "BQACAg...",
  "post_no": 19,
  "chat_id": 123,
  "msg1_id": 1001,
  "msg2_id": 1002,
  "click_message_id": 1003 (optional),
  "delete_after": <datetime>
}

Run via CRON every minute:
    * * * * * /usr/bin/python3 /path/to/cleanup_files.py
"""

import sys
import logging

sys.path.append(".")

import asyncio
from aiogram import Bot
from core.database import init_db, db
from core.utils.time_utils import now
from core.config import config
from core.utils.logger import get_job_logger


logger = get_job_logger("cleanup_files")


async def cleanup_files():
    logger.info("---- Cleanup File Delivery Job Started ----")

    bot = Bot(token=config.BOT_B_TOKEN, parse_mode="Markdown")

    current = now()

    # Find all expired entries
    expired_entries = db.temp_delivery.find({
        "delete_after": {"$lt": current}
    })

    delete_count = 0

    async for entry in expired_entries:
        chat_id = entry.get("chat_id")
        msg1_id = entry.get("msg1_id")
        msg2_id = entry.get("msg2_id")
        click_id = entry.get("click_message_id")  # optional

        # ----------------------------------------------
        # Delete Message #1
        # ----------------------------------------------
        try:
            await bot.delete_message(chat_id, msg1_id)
            logger.info(f"Deleted file message 1: {msg1_id}")
        except Exception:
            pass

        # ----------------------------------------------
        # Delete Message #2
        # ----------------------------------------------
        try:
            await bot.delete_message(chat_id, msg2_id)
            logger.info(f"Deleted file message 2: {msg2_id}")
        except Exception:
            pass

        # ----------------------------------------------
        # Delete post-download "Click Here" message
        # ----------------------------------------------
        if click_id:
            try:
                await bot.delete_message(chat_id, click_id)
                logger.info(f"Deleted click message: {click_id}")
            except Exception:
                pass

        # ----------------------------------------------
        # Remove this entry from DB
        # ----------------------------------------------
        db.temp_delivery.delete_one({"_id": entry["_id"]})
        delete_count += 1

    logger.info(f"Expired deliveries cleaned: {delete_count}")
    logger.info("---- Cleanup Files Job Completed ✔ ----")


if __name__ == "__main__":
    init_db()
    asyncio.run(cleanup_files())
