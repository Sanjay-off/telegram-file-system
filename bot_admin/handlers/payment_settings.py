# bot_admin/handlers/payment_settings.py

from aiogram import Router, types
from aiogram.filters import Command
from bot_admin.utils.helpers import is_admin
from core.database import db

router = Router()


# ---------------------------------------------------
# Set UPI ID
# ---------------------------------------------------
@router.message(Command("setupi"))
async def set_upi(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("⚠ Usage:\n`/setupi yourupi@upi`", parse_mode="Markdown")

    upi = parts[1].strip()

    db.settings.update_one(
        {"key": "upi_id"},
        {"$set": {"value": upi}},
        upsert=True
    )

    await message.reply(
        f"✅ **UPI ID updated successfully!**\n\n"
        f"💳 New UPI ID: `{upi}`",
        parse_mode="Markdown"
    )


# ---------------------------------------------------
# Set UPI Display Name
# ---------------------------------------------------
@router.message(Command("setpayname"))
async def set_pay_name(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("⚠ Usage:\n`/setpayname SANJAY P`", parse_mode="Markdown")

    name = parts[1].strip()

    db.settings.update_one(
        {"key": "upi_name"},
        {"$set": {"value": name}},
        upsert=True
    )

    await message.reply(
        f"📝 **UPI Name updated successfully!**\n\n"
        f"👤 Display Name: `{name}`",
        parse_mode="Markdown"
    )


# ---------------------------------------------------
# Set QR Expiry Time
# ---------------------------------------------------
@router.message(Command("setqrexpiry"))
async def set_qr_expiry(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply("⚠ Usage:\n`/setqrexpiry <minutes>`", parse_mode="Markdown")

    try:
        minutes = int(parts[1])
    except:
        return await message.reply("❌ QR expiry must be a number.")

    if minutes <= 0:
        return await message.reply("❌ Minutes must be greater than 0.")

    db.settings.update_one(
        {"key": "qr_expiry"},
        {"$set": {"value": minutes}},
        upsert=True
    )

    await message.reply(
        f"⏱ **QR Expiry Updated!**\n"
        f"Valid for `{minutes}` minutes.",
        parse_mode="Markdown"
    )


# ---------------------------------------------------
# Auto Confirm ON/OFF
# ---------------------------------------------------
@router.message(Command("autoconfirm"))
async def auto_confirm(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply(
            "⚠ Usage:\n`/autoconfirm on` or `/autoconfirm off`",
            parse_mode="Markdown"
        )

    mode = parts[1].lower()

    if mode not in ["on", "off"]:
        return await message.reply("❌ Choose `on` or `off` only.")

    db.settings.update_one(
        {"key": "auto_confirm"},
        {"$set": {"value": mode}},
        upsert=True
    )

    await message.reply(
        f"🔧 Auto-Confirm is now **{mode.upper()}**.",
        parse_mode="Markdown"
    )


# ---------------------------------------------------
# Manual / Auto Payment Mode
# ---------------------------------------------------
@router.message(Command("setpaymentmode"))
async def set_payment_mode(message: types.Message):
    """
    manual → Admin must confirm order
    auto → Auto-confirm after 10 hours (your custom logic)
    """
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply(
            "⚠ Usage:\n`/setpaymentmode manual` or `/setpaymentmode auto`",
            parse_mode="Markdown"
        )

    mode = parts[1].lower()

    if mode not in ["manual", "auto"]:
        return await message.reply("❌ Choose `manual` or `auto` only.")

    db.settings.update_one(
        {"key": "payment_mode"},
        {"$set": {"value": mode}},
        upsert=True
    )

    await message.reply(
        f"💼 Payment mode set to: **{mode.upper()}**",
        parse_mode="Markdown"
    )


# ---------------------------------------------------
# Unique Paise Price (on/off)
# ---------------------------------------------------
@router.message(Command("uniqueprice"))
async def unique_price_toggle(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply(
            "⚠ Usage:\n`/uniqueprice on` or `/uniqueprice off`",
            parse_mode="Markdown"
        )

    mode = parts[1].lower()

    if mode not in ["on", "off"]:
        return await message.reply("❌ Choose `on` or `off` only.")

    db.settings.update_one(
        {"key": "unique_paise"},
        {"$set": {"value": mode}},
        upsert=True
    )

    await message.reply(
        f"💰 Unique Price Mode: **{mode.upper()}**",
        parse_mode="Markdown"
    )


# ---------------------------------------------------
# Allow Screenshot Proof (on/off)
# ---------------------------------------------------
@router.message(Command("allowproof"))
async def allow_proof_toggle(message: types.Message):
    if not await is_admin(message.from_user.id):
        return

    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply(
            "⚠ Usage:\n`/allowproof on` or `/allowproof off`",
            parse_mode="Markdown"
        )

    mode = parts[1].lower()

    if mode not in ["on", "off"]:
        return await message.reply("❌ Choose `on` or `off` only.")

    db.settings.update_one(
        {"key": "allow_proof"},
        {"$set": {"value": mode}},
        upsert=True
    )

    await message.reply(
        f"📷 Screenshot Proof: **{mode.upper()}**",
        parse_mode="Markdown"
    )
