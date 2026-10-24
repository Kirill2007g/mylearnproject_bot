import asyncio

from src.mylearnprojectbot.config import settings
from aiogram import Bot, Dispatcher
from handlers import start


bot = Bot(token=settings.BOT_TOKEN.get_secret_value())
dp = Dispatcher()

dp.include_router(start.router)



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())