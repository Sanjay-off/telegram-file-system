# bot_admin/handlers/menu.py

from aiogram import Router, types
from aiogram.filters import Command
from bot_admin.utils.helpers import is_admin

router = Router()


@router.message(Command("menu"))
async def admin_menu(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            # ------------------- FILE SYSTEM -------------------
            [
                types.InlineKeyboardButton(
                    text="📁 Add File",
                    callback_data="menu_addfile"
                ),
                types.InlineKeyboardButton(
                    text="📄 List Files",
                    callback_data="menu_listfiles"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="🗑 Delete File",
                    callback_data="menu_deletefile"
                )
            ],

            # ------------------- FORCE SUBSCRIBE -------------------
            [
                types.InlineKeyboardButton(
                    text="🔗 Add FS Channel",
                    callback_data="menu_addforce"
                ),
                types.InlineKeyboardButton(
                    text="📋 List FS Channels",
                    callback_data="menu_listforce"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="❌ Remove FS Channel",
                    callback_data="menu_removeforce"
                )
            ],

            # ------------------- VERIFICATION SETTINGS -------------------
            [
                types.InlineKeyboardButton(
                    text="📝 Set Verify Guide",
                    callback_data="menu_set_guide"
                ),
                types.InlineKeyboardButton(
                    text="👁 Show Guide",
                    callback_data="menu_show_guide"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="⏳ Grant Verify (Hours)",
                    callback_data="menu_grantverify"
                )
            ],

            # ------------------- PREMIUM SYSTEM -------------------
            [
                types.InlineKeyboardButton(
                    text="💎 Add Plan",
                    callback_data="menu_addplan"
                ),
                types.InlineKeyboardButton(
                    text="📌 List Plans",
                    callback_data="menu_listplans"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="❌ Remove Plan",
                    callback_data="menu_removeplan"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="⏱ Set QR Expiry",
                    callback_data="menu_setexpiry"
                ),
                types.InlineKeyboardButton(
                    text="🔧 Auto-Confirm ON/OFF",
                    callback_data="menu_autoconfirm"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="📦 Pending Orders",
                    callback_data="menu_orders"
                ),
                types.InlineKeyboardButton(
                    text="✔ Confirm Order",
                    callback_data="menu_confirmorder"
                ),
            ],

            # ------------------- SHORTENER SETTINGS -------------------
            [
                types.InlineKeyboardButton(
                    text="➕ Add Shortener",
                    callback_data="menu_addshortener"
                ),
                types.InlineKeyboardButton(
                    text="📜 List Shorteners",
                    callback_data="menu_listshorteners"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="❌ Remove Shortener",
                    callback_data="menu_removeshortener"
                )
            ],

            # ------------------- ADMIN SETTINGS -------------------
            [
                types.InlineKeyboardButton(
                    text="👑 Add Admin",
                    callback_data="menu_addadmin"
                ),
                types.InlineKeyboardButton(
                    text="📋 List Admins",
                    callback_data="menu_listadmins"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="❌ Remove Admin",
                    callback_data="menu_removeadmin"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="☎ Set Admin Contact",
                    callback_data="menu_setadmincontact"
                )
            ],

            # ------------------- BROADCAST SYSTEM -------------------
            [
                types.InlineKeyboardButton(
                    text="📢 Broadcast",
                    callback_data="menu_broadcast"
                )
            ],

            # ------------------- STATS -------------------
            [
                types.InlineKeyboardButton(
                    text="📊 Show Stats",
                    callback_data="menu_stats"
                )
            ]
        ]
    )

    await message.reply(
        "🛠 **Admin Control Panel**\n"
        "Choose an option below:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
