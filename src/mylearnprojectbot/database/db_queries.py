from sqlalchemy import select, insert, update, delete
from db import async_session
from models import Record
from datetime import datetime

async def add_record(fsm_data: dict):
    async with async_session() as session:
        new_record = insert(Record).values(
            subject=fsm_data[0],
            topic=fsm_data[1],
            ration=fsm_data[2],
            completed_date=datetime.now(),
        )
        await session.execute(new_record)
        await session.commit()

