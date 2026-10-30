from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from mylearnprojectbot.database.db_queries import RecordQueries
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
    photo = FSInputFile(base_dir / "files" / "add_command_example.png")
    await message.answer_photo(photo, caption="Как использовать /add")
    parts = [p.strip() for p in re.split(r"[;\n]+", command.args or "") if p.strip()]
    if len(parts) < 3:
        await message.answer("Нужно 3 поля: subject;\ntopic;\nration;")
        return

    await state.update_data(subject=parts[0], topic=parts[1], ration=parts[2], date=datetime.today())
    data = await state.get_data()
    await RecordQueries.add_record(data)
    await message.answer("✅ Запись добавлена")


@router.message(Command("show"), CheckIfCommandExists())
async def cmd_show(message: Message, state: FSMContext, command: CommandObject):
    date = await match_re_search(text=message.text)
    record = await RecordQueries.show_record(date)
    await message.answer(f"Record: {str(record)}")

@router.message(Command("delete"), CheckIfCommandExists())
async def cmd_delete(message: Message, state: FSMContext, command: CommandObject):
    date = await match_re_search(text=message.text)
    record = await RecordQueries.delete_record(date)
    await message.answer(record)

@router.message(Command("complete"), CheckIfCommandExists())
async def cmd_complete(message: Message, state: FSMContext, command: CommandObject):
    date = await match_re_search(text=message.text)
    await RecordQueries.make_record_competed(date)

async def match_re_search(text):
    match = re.search(r"\d{4}-\d{2}-\d{2}", text)
    if match:
        date = match.group(0)
        date = datetime.strptime(date, "%Y-%m-%d")
        return date
    return None