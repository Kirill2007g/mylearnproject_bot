import asyncio

from mylearnprojectbot.database.db import Base, engine
from mylearnprojectbot.database.models import Record   # noqa: F401

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

if __name__ == '__main__':
    asyncio.run(init_db())