from aiogram.filters import BaseFilter, CommandObject
from aiogram.types import Message


class CheckIfCommandExists(BaseFilter):
    async def __call__(self, message: Message, command: CommandObject):
        if not command.args:
            print(f"Введите текст после команды: {command.command}")
            return False
        return True