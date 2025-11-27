# bot_user/user_main.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from bot_user import setup_user_handlers
from core.config import config
from core.database import init_db


async def main():
    # ---------------------------------------------------
    # LOGGING CONFIGURATION
    # ---------------------------------------------------
    logging.basicConfig(
        filename="logs/user_bot.log",
        level=logging.INFO,
        format="[USER BOT] %(asctime)s - %(levelname)s - %(message)s"
    )

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger().addHandler(console)

    logging.info("🚀 Starting User Bot...")

    # ---------------------------------------------------
    # INIT DATABASE CONNECTION
    # ---------------------------------------------------
    init_db()

    # ---------------------------------------------------
    # INIT BOT WITH PARSE MODE
    # ---------------------------------------------------
    bot = Bot(
        token=config.BOT_B_TOKEN,
        parse_mode=ParseMode.MARKDOWN
    )

    dp = Dispatcher()

    # ---------------------------------------------------
    # REGISTER ALL USER BOT ROUTERS
    # ---------------------------------------------------
    dp.include_router(setup_user_handlers())

    logging.info("User Bot Handlers Loaded Successfully.")

    # ---------------------------------------------------
    # START POLLING
    # ---------------------------------------------------
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"❌ Polling crashed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
