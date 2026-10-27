from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from mylearnprojectbot.database.db_queries import add_record, delete_record, show_record, make_record_competed
from datetime import datetime
from mylearnprojectbot.filters.handlers_filters import CheckIfCommandExists
from pathlib import Path
import re

router = Router()
base_dir = Path(__file__).resolve().parent.parent

@router.message(F.photo | F.video | F.video_note)
async def capture_media(message: Message):
    if message.photo:
        await message.answer(message.photo[-1].file_id)

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет")


@router.message(Command("add"))
async def cmd_add(message: Message, state: FSMContext, command: CommandObject):
    photo_path = base_dir / "files" / "add_command_example.png"
    photo = FSInputFile(photo_path)
    await message.answer_photo(
        photo,
        caption="Как использовать /add"
    )
    user_input = [p.strip() for p in re.split(r"[;\n]", command.args)]
    await state.update_data(subject=user_input[0], topic=user_input[1], ration=user_input[2], date=datetime.today())
    data = await state.get_data()
    await add_record(data)


@router.message(Command("show"), CheckIfCommandExists())
async def cmd_show(message: Message, state: FSMContext, command: CommandObject):
    date = await match_re_search(text=message.text)
    record = await show_record(date)
    await message.answer(f"Record: {str(record)}")

@router.message(Command("delete"), CheckIfCommandExists())
async def cmd_delete(message: Message, state: FSMContext, command: CommandObject):
    date = await match_re_search(text=message.text)
    record = await delete_record(date)
    await message.answer(record)

@router.message(Command("complete"), CheckIfCommandExists())
async def cmd_complete(message: Message, state: FSMContext, command: CommandObject):
    date = await match_re_search(text=message.text)
    await make_record_competed(date)

async def match_re_search(text):
    match = re.search(r"\d{4}-\d{2}-\d{2}", text)
    if match:
        date = match.group(0)
        date = datetime.strptime(date, "%Y-%m-%d")
        return date
    return None