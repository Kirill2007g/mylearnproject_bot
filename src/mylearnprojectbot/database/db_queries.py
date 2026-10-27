from sqlalchemy import select, insert, cast, Date, update, delete
from mylearnprojectbot.database.db import async_session
from mylearnprojectbot.database.models import Record


async def add_record(fsm_data: dict):
    subject_ = fsm_data.get('subject')
    topic_ = fsm_data.get('topic')
    ration_ = fsm_data.get('ration')
    date_ = fsm_data.get('date')
    async with async_session() as session:
        new_record = insert(Record).values(
            subject=subject_,
            topic=topic_,
            ration=ration_,
            date=date_,
        )
        await session.execute(new_record)
        await session.commit()

async def get_record(date) -> Record:
    async with async_session() as session:
        show_record_ = select(Record).where(cast(Record.date, Date) == date.date())
        result = await session.execute(show_record_)
        print(result)
        return result.scalar_one_or_none()

async def show_record(date):
    record = await get_record(date)
    print(record)
    return record.show_record if record else None


async def delete_record(date):
    async with async_session() as session:
        delete_record_ = delete(Record).where(cast(Record.date, Date) == date.date())
        await session.execute(delete_record_)
        await session.commit()

async def make_record_competed(date):
    async with async_session() as session:
        stmt = update(Record).where(cast(Record.date, Date) == date.date()).values(completed=True)
        await session.execute(stmt)
        await session.commit()
