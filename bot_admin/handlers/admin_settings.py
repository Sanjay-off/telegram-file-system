# bot_admin/handlers/admin_settings.py

from aiogram import Router, types
from aiogram.filters import Command
from core.database import db
from core.config import config
from core.utils.logger import log
from core.utils.time_utils import now
from bot_admin.utils.helpers import is_admin

router = Router()


# ---------------------------
# ADD ADMIN
# ---------------------------
@router.message(Command("addadmin"))
async def add_admin(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply("⚠ Usage: /addadmin <user_id>")

    try:
        new_admin = int(parts[1])
    except:
        return await message.reply("❌ Invalid user ID.")

    # Insert into DB if not exists
    db.settings.update_one(
        {"key": "admins"},
        {"$addToSet": {"value": new_admin}},
        upsert=True
    )

    await message.reply(f"✅ Added admin: `{new_admin}`", parse_mode="Markdown")


# ---------------------------
# REMOVE ADMIN
# ---------------------------
@router.message(Command("removeadmin"))
async def remove_admin(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply("⚠ Usage: /removeadmin <user_id>")

    try:
        remove_admin_id = int(parts[1])
    except:
        return await message.reply("❌ Invalid user ID.")

    db.settings.update_one(
        {"key": "admins"},
        {"$pull": {"value": remove_admin_id}}
    )

    await message.reply(f"🗑 Removed admin: `{remove_admin_id}`", parse_mode="Markdown")


# ---------------------------
# LIST ADMINS
# ---------------------------
@router.message(Command("listadmins"))
async def list_admins(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    doc = db.settings.find_one({"key": "admins"})
    admins = doc["value"] if doc else []

    if not admins:
        return await message.reply("⚠ No admins set.")

    text = "👑 **Admins List:**\n\n"
    for adm in admins:
        text += f"• `{adm}`\n"

    await message.reply(text, parse_mode="Markdown")


# ---------------------------
# SET ADMIN CONTACT (For users)
# ---------------------------
@router.message(Command("setadmin"))
async def set_admin_contact(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply("⚠ Usage: /setadmin <user_id | @username>")

    admin_contact = parts[1]

    db.settings.update_one(
        {"key": "admin_contact"},
        {"$set": {"value": admin_contact}},
        upsert=True
    )

    await message.reply(f"📞 Admin contact updated to: `{admin_contact}`", parse_mode="Markdown")


# ---------------------------
# GET ADMIN CONTACT
# ---------------------------
@router.message(Command("getadmin"))
async def get_admin_contact(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    doc = db.settings.find_one({"key": "admin_contact"})
    contact = doc["value"] if doc else "Not set"

    await message.reply(f"📞 Current admin contact: `{contact}`", parse_mode="Markdown")

