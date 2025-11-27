# bot_admin/admin_main.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from bot_admin import setup_admin_handlers
from core.config import config
from core.database import init_db


async def main():
    # ---------------------------------------------------
    # LOGGING
    # ---------------------------------------------------
    logging.basicConfig(
        level=logging.INFO,
        format="[ADMIN BOT] %(asctime)s - %(levelname)s - %(message)s"
    )

    # ---------------------------------------------------
    # INIT DATABASE
    # ---------------------------------------------------
    init_db()  # connects to your MongoDB (local or cloud)

    # ---------------------------------------------------
    # INIT BOT
    # ---------------------------------------------------
    bot = Bot(
        token=config.BOT_A_TOKEN,
        parse_mode=ParseMode.MARKDOWN
    )

    dp = Dispatcher()

    # ---------------------------------------------------
    # REGISTER ALL ADMIN HANDLERS
    # ---------------------------------------------------
    dp.include_router(setup_admin_handlers())

    logging.info("Admin Bot Started Successfully 🚀")

    # ---------------------------------------------------
    # START POLLING
    # ---------------------------------------------------
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Error while polling: {e}")


if __name__ == "__main__":
    asyncio.run(main())
