# bot_admin/keyboards/menu_keyboard.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_main_keyboard():
    """
    Reply keyboard (bottom keyboard) for Admin Bot.
    Appears when admin uses /start.
    """

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="/menu"),
                KeyboardButton(text="/stats")
            ],
            [
                KeyboardButton(text="/orders"),
                KeyboardButton(text="/broadcast")
            ]
        ],
        resize_keyboard=True
    )

    return keyboard
