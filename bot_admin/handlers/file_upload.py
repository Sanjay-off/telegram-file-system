# bot_admin/handlers/file_upload.py

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot_admin.utils.helpers import is_admin, generate_file_db_id
from core.database import db

router = Router()


# ----------------------------------------------------
# STATE MACHINE FOR FILE UPLOAD FLOW
# ----------------------------------------------------
class UploadStates(StatesGroup):
    waiting_for_file = State()
    waiting_for_post_no = State()
    waiting_for_description = State()
    waiting_for_extra_message = State()


# ----------------------------------------------------
# START FILE UPLOAD PROCESS
# ----------------------------------------------------
@router.message(Command("addfile"))
async def start_file_upload(message: types.Message, state: FSMContext):
    if not await is_admin(message.from_user.id):
        return
    
    await state.set_state(UploadStates.waiting_for_file)
    await message.reply(
        "📁 **Send the ZIP file to upload**.\n\n"
        "➡️ After uploading, I will ask for Post No, Description and Extra Message.",
        parse_mode="Markdown"
    )


# ----------------------------------------------------
# STEP 1 — RECEIVE ZIP FILE
# ----------------------------------------------------
@router.message(UploadStates.waiting_for_file, F.document)
async def receive_zip(message: types.Message, state: FSMContext):
    if not await is_admin(message.from_user.id):
        return
    
    document = message.document
    
    if not document.file_name.endswith(".zip"):
        return await message.reply("❌ Only **ZIP files** are allowed!")

    file_id = document.file_id

    # Store in temporary FSM memory
    await state.update_data(file_id=file_id)

    await state.set_state(UploadStates.waiting_for_post_no)
    await message.reply("🔢 **Enter Post Number**:", parse_mode="Markdown")


# ----------------------------------------------------
# STEP 2 — RECEIVE POST NUMBER
# ----------------------------------------------------
@router.message(UploadStates.waiting_for_post_no)
async def receive_post_no(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.reply("❌ Post No must be a number.")

    await state.update_data(post_no=int(message.text))
    await state.set_state(UploadStates.waiting_for_description)

    await message.reply("📝 **Enter Description**:", parse_mode="Markdown")


# ----------------------------------------------------
# STEP 3 — RECEIVE DESCRIPTION
# ----------------------------------------------------
@router.message(UploadStates.waiting_for_description)
async def receive_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(UploadStates.waiting_for_extra_message)

    await message.reply("🗒 **Enter Extra Message**:", parse_mode="Markdown")


# ----------------------------------------------------
# STEP 4 — RECEIVE EXTRA MESSAGE AND SAVE TO DB
# ----------------------------------------------------
@router.message(UploadStates.waiting_for_extra_message)
async def receive_extra(message: types.Message, state: FSMContext):
    data = await state.get_data()

    file_db_id = generate_file_db_id()

    file_info = {
        "file_db_id": file_db_id,
        "file_id": data["file_id"],
        "post_no": data["post_no"],
        "description": data["description"],
        "extra_message": message.text,
    }

    # Store in DB
    db.files.insert_one(file_info)

    await message.reply(
        f"✅ **File Saved Successfully!**\n\n"
        f"📌 File DB ID: `{file_db_id}`\n"
        f"➡️ Use `/gentemplate {file_db_id}` to generate the public template.",
        parse_mode="Markdown"
    )

    await state.clear()
