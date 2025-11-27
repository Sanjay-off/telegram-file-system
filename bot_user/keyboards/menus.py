# bot_user/keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def user_main_menu():
    """
    Bottom menu keyboard for Bot B (File Delivery Bot).
    Appears when user types /start.
    """

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="/start"),
                KeyboardButton(text="/help")
            ],
            [
                KeyboardButton(text="/checkpremium"),
                KeyboardButton(text="/id")
            ]
        ],
        resize_keyboard=True
    )

    return keyboard
