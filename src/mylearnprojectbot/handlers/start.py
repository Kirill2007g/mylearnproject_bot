from aiogram import Router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from mylearnprojectbot.database.db_queries import add_record

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет")

@router.message(Command("add"))
async def cmd_add(message: Message, state: FSMContext, command: CommandObject):
    if not command.args:
        await message.answer("Введи текст после команды /add")
        return
    user_text = command.args.split(";" and "\n")
    data = state.update_data(user_text=user_text)
    # print(f"message.text: {message.text}, {type(message.text)}")
    # print()
    # print(user_text)

@router.message(Command("show"))
async def cmd_show(message: Message, state: FSMContext, command: Command):
    pass