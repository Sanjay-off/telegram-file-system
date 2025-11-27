# bot_admin/keyboards/inline_keyboards.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ---------------------------------------------------
# FILE SYSTEM KEYBOARD
# ---------------------------------------------------
def file_system_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📁 Add File", callback_data="menu_addfile"),
                InlineKeyboardButton(text="📄 List Files", callback_data="menu_listfiles")
            ],
            [
                InlineKeyboardButton(text="🗑 Delete File", callback_data="menu_deletefile")
            ],
            [
                InlineKeyboardButton(text="⬅ Back", callback_data="menu_main")
            ]
        ]
    )


# ---------------------------------------------------
# FORCE SUBSCRIBE KEYBOARD
# ---------------------------------------------------
def force_sub_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➕ Add Channel", callback_data="menu_addforce"),
                InlineKeyboardButton(text="📜 List Channels", callback_data="menu_listforce")
            ],
            [
                InlineKeyboardButton(text="❌ Remove Channel", callback_data="menu_removeforce")
            ],
            [
                InlineKeyboardButton(text="⬅ Back", callback_data="menu_main")
            ]
        ]
    )


# ---------------------------------------------------
# VERIFICATION SETTINGS KEYBOARD
# ---------------------------------------------------
def verification_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📝 Set Guide", callback_data="menu_set_guide"),
                InlineKeyboardButton(text="👁 Show Guide", callback_data="menu_show_guide")
            ],
            [
                InlineKeyboardButton(text="⏳ Grant Verify", callback_data="menu_grantverify")
            ],
            [
                InlineKeyboardButton(text="⬅ Back", callback_data="menu_main")
            ]
        ]
    )


# ---------------------------------------------------
# PREMIUM SYSTEM KEYBOARD
# ---------------------------------------------------
def premium_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💎 Add Plan", callback_data="menu_addplan"),
                InlineKeyboardButton(text="📌 List Plans", callback_data="menu_listplans")
            ],
            [
                InlineKeyboardButton(text="❌ Remove Plan", callback_data="menu_removeplan")
            ],
            [
                InlineKeyboardButton(text="⏱ Set QR Expiry", callback_data="menu_setexpiry"),
                InlineKeyboardButton(text="🔧 Auto-Confirm ON/OFF", callback_data="menu_autoconfirm")
            ],
            [
                InlineKeyboardButton(text="📦 Pending Orders", callback_data="menu_orders"),
                InlineKeyboardButton(text="✔ Confirm Order", callback_data="menu_confirmorder")
            ],
            [
                InlineKeyboardButton(text="⬅ Back", callback_data="menu_main")
            ]
        ]
    )


# ---------------------------------------------------
# SHORTENER KEYBOARD
# ---------------------------------------------------
def shortener_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➕ Add Shortener", callback_data="menu_addshortener"),
                InlineKeyboardButton(text="📜 List Shorteners", callback_data="menu_listshorteners")
            ],
            [
                InlineKeyboardButton(text="❌ Remove Shortener", callback_data="menu_removeshortener")
            ],
            [
                InlineKeyboardButton(text="⬅ Back", callback_data="menu_main")
            ]
        ]
    )


# ---------------------------------------------------
# ADMIN SETTINGS KEYBOARD
# ---------------------------------------------------
def admin_settings_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👑 Add Admin", callback_data="menu_addadmin"),
                InlineKeyboardButton(text="📋 List Admins", callback_data="menu_listadmins")
            ],
            [
                InlineKeyboardButton(text="❌ Remove Admin", callback_data="menu_removeadmin")
            ],
            [
                InlineKeyboardButton(text="☎ Set Admin Contact", callback_data="menu_setadmincontact")
            ],
            [
                InlineKeyboardButton(text="⬅ Back", callback_data="menu_main")
            ]
        ]
    )


# ---------------------------------------------------
# BROADCAST KEYBOARD
# ---------------------------------------------------
def broadcast_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📢 Broadcast", callback_data="menu_broadcast")
            ],
            [
                InlineKeyboardButton(text="⬅ Back", callback_data="menu_main")
            ]
        ]
    )


# ---------------------------------------------------
# STATS KEYBOARD
# ---------------------------------------------------
def stats_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📊 Show Stats", callback_data="menu_stats")
            ],
            [
                InlineKeyboardButton(text="⬅ Back", callback_data="menu_main")
            ]
        ]
    )


# ---------------------------------------------------
# MAIN ADMIN MENU (called from /menu)
# ---------------------------------------------------
def main_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📁 File System", callback_data="menu_files"),
                InlineKeyboardButton(text="🔗 Force Subscribe", callback_data="menu_forcesub")
            ],
            [
                InlineKeyboardButton(text="📝 Verification", callback_data="menu_verification"),
                InlineKeyboardButton(text="💎 Premium System", callback_data="menu_premium")
            ],
            [
                InlineKeyboardButton(text="🔗 Shorteners", callback_data="menu_shortener"),
            ],
            [
                InlineKeyboardButton(text="👑 Admin Settings", callback_data="menu_adminsettings")
            ],
            [
                InlineKeyboardButton(text="📢 Broadcast", callback_data="menu_broadcast")
            ],
            [
                InlineKeyboardButton(text="📊 Stats", callback_data="menu_stats")
            ]
        ]
    )
