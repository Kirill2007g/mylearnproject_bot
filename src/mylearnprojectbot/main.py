import asyncio
from aiogram.types import BotCommand
from mylearnprojectbot.config import settings
from aiogram import Bot, Dispatcher
from mylearnprojectbot.handlers import main_commands


bot = Bot(token=settings.BOT_TOKEN.get_secret_value())
dp = Dispatcher()

dp.include_router(main_commands.router)

async def set_main_commands(bot: Bot):
    commands = [
        BotCommand(command="/help", description="Справка и помощь"),
        BotCommand(command="/add", description="Добавить запись в базу данных"),
        BotCommand(command="/show", description="Посмотреть запись по дате"),
        BotCommand(command="/delete", description="Удалить запись по дате"),
        BotCommand(command="/complete", description="Отметить добавленную запись как выполненую")
    ]
    await bot.set_my_commands(commands)
async def main():
    dp.startup.register(set_main_commands)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())