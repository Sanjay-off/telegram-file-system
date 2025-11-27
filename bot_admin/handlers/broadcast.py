# bot_admin/handlers/broadcast.py

from aiogram import Router, types
from aiogram.filters import Command
from core.database import db
from bot_admin.utils.helpers import is_admin
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
import asyncio

router = Router()


# ---------------------------------------------------
# Helper: broadcast send function
# ---------------------------------------------------
async def broadcast_message(bot, msg, content_type="text", file=None):
    users = db.users.find({}, {"user_id": 1})

    total = 0
    success = 0
    failed = 0

    for user in users:
        uid = user["user_id"]
        total += 1

        try:
            if content_type == "text":
                await bot.send_message(uid, msg)
            elif content_type == "photo":
                await bot.send_photo(uid, file, caption=msg)
            elif content_type == "file":
                await bot.send_document(uid, file, caption=msg)

            success += 1

        except (TelegramForbiddenError, TelegramBadRequest):
            failed += 1

        await asyncio.sleep(1)   # SAFE LIMIT (1 msg per second)

    return total, success, failed


# ---------------------------------------------------
# /broadcast → text broadcast
# ---------------------------------------------------
@router.message(Command("broadcast"))
async def broadcast_start(message: types.Message, bot):
    if not await is_admin(message.from_user.id):
        return

    await message.reply(
        "📣 **Broadcast Mode Activated**\n\n"
        "Send me the message you want to broadcast to all users.\n"
        "⚠ Only text is allowed in this command.\n",
        parse_mode="Markdown"
    )

    @router.message()
    async def process_broadcast_text(msg: types.Message):
        if not await is_admin(msg.from_user.id):
            return
        
        text = msg.text
        await msg.reply("📤 Broadcasting... This may take a while.")

        total, success, failed = await broadcast_message(bot, text)

        return await msg.reply(
            f"📊 **Broadcast Completed**\n\n"
            f"👥 Total Users: {total}\n"
            f"✅ Delivered: {success}\n"
            f"❌ Failed: {failed}",
            parse_mode="Markdown"
        )


# ---------------------------------------------------
# /broadcastphoto → photo broadcast
# ---------------------------------------------------
@router.message(Command("broadcastphoto"))
async def broadcast_photo(message: types.Message, bot):
    if not await is_admin(message.from_user.id):
        return

    await message.reply(
        "📸 Send the **photo** with caption to broadcast.\n"
        "⚠ Only one photo allowed.",
        parse_mode="Markdown"
    )

    @router.message()
    async def process_broadcast_photo(msg: types.Message):
        if not await is_admin(msg.from_user.id):
            return

        if not msg.photo:
            return await msg.reply("❌ Please send a photo.")

        photo = msg.photo[-1].file_id
        caption = msg.caption or ""

        await msg.reply("📤 Broadcasting photo...")

        total, success, failed = await broadcast_message(
            bot, caption, content_type="photo", file=photo
        )

        return await msg.reply(
            f"📊 **Broadcast Completed**\n\n"
            f"👥 Total Users: {total}\n"
            f"✅ Delivered: {success}\n"
            f"❌ Failed: {failed}",
            parse_mode="Markdown"
        )


# ---------------------------------------------------
# /broadcastfile → documents/videos broadcast
# ---------------------------------------------------
@router.message(Command("broadcastfile"))
async def broadcast_file(message: types.Message, bot):
    if not await is_admin(message.from_user.id):
        return
    
    await message.reply(
        "📁 Send the **document or video** with caption to broadcast.\n"
        "⚠ Only one file allowed.",
        parse_mode="Markdown"
    )

    @router.message()
    async def process_broadcast_doc(msg: types.Message):
        if not await is_admin(msg.from_user.id):
            return

        if not msg.document and not msg.video:
            return await msg.reply("❌ Please send a document or video.")

        file = msg.document.file_id if msg.document else msg.video.file_id
        caption = msg.caption or ""

        await msg.reply("📤 Broadcasting file...")

        total, success, failed = await broadcast_message(
            bot, caption, content_type="file", file=file
        )

        return await msg.reply(
            f"📊 **Broadcast Completed**\n\n"
            f"👥 Total Users: {total}\n"
            f"✅ Delivered: {success}\n"
            f"❌ Failed: {failed}",
            parse_mode="Markdown"
        )
