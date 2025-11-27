# bot_admin/handlers/start.py

from aiogram import Router, types
from aiogram.filters import Command
from bot_admin.utils.helpers import is_admin

router = Router()


@router.message(Command("start"))
async def admin_start(message: types.Message):
    user_id = message.from_user.id

    if not await is_admin(user_id):
        return await message.reply(
            "❌ **Access Denied**\n\n"
            "You are not an admin of this bot.",
            parse_mode="Markdown"
        )

    text = (
        f"👋 **Hello, Admin!**\n"
        f"Welcome to the **Admin Control Bot**.\n\n"
        f"Use the panel below to manage your system.\n\n"
        f"🛠 Commands:\n"
        f"• `/menu` — Open Admin Menu\n"
        f"• `/addfile` — Upload ZIP & add file\n"
        f"• `/orders` — View pending orders\n"
        f"• `/stats` — Bot statistics\n"
        f"• `/broadcast` — Broadcast to all users\n"
    )

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="/menu"),
                types.KeyboardButton(text="/stats")
            ],
            [
                types.KeyboardButton(text="/orders"),
                types.KeyboardButton(text="/broadcast")
            ],
        ],
        resize_keyboard=True
    )

    await message.reply(text, reply_markup=keyboard, parse_mode="Markdown")
