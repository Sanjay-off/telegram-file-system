# bot_user/handlers/checkpremium.py

from aiogram import Router, types
from aiogram.filters import Command
from core.database import db
from core.utils.time_utils import now
from bot_admin.services.premium_service import PremiumService

router = Router()


@router.message(Command("checkpremium"))
async def check_premium(message: types.Message):
    """
    Shows premium status for user.
    """

    user_id = message.from_user.id
    current_time = now()

    user = db.users.find_one({"user_id": user_id})

    # -----------------------------------------
    # USER NOT FOUND IN DB → Not premium
    # -----------------------------------------
    if not user or not user.get("is_premium"):
        return await message.reply(
            "💎 **Premium Status:** NOT ACTIVE\n\n"
            "›› You do not have an active premium plan.\n"
            "›› Use the premium menu to upgrade.",
            parse_mode="Markdown"
        )

    expiry = user.get("premium_expiry")

    # -----------------------------------------
    # EXPIRED → Clean up premium
    # -----------------------------------------
    if expiry <= current_time:
        # Remove premium status
        PremiumService.revoke_premium(user_id)

        return await message.reply(
            "💎 **Premium Status:** EXPIRED\n\n"
            "›› Your premium plan has expired.\n"
            "›› Renew to continue using premium features.",
            parse_mode="Markdown"
        )

    # -----------------------------------------
    # STILL ACTIVE → Show expiry
    # -----------------------------------------
    remaining = expiry - current_time
    days = remaining.days
    hours = remaining.seconds // 3600
    minutes = (remaining.seconds % 3600) // 60

    await message.reply(
        "💎 **Premium Status: ACTIVE**\n\n"
        f"📅 **Expires On:** `{expiry}`\n"
        f"⏳ **Remaining:** `{days} days, {hours} hours, {minutes} minutes`",
        parse_mode="Markdown"
    )
