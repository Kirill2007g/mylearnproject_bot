from sqlalchemy import select, insert, cast, Date, update, delete
from mylearnprojectbot.database.db import async_session
from mylearnprojectbot.database.models import Record
import logging
import json
from datetime import datetime, timezone
logger = logging.getLogger(name="query_logger")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("C:\\Users\\User\\Desktop\\mylearnprojectbotlogs.txt", encoding="utf-8", mode="a")
handler.setLevel(logging.INFO)


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:

        log_data = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "logger": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False, default=str)

handler.setFormatter(JSONFormatter())
logger.addHandler(handler)


class RecordQueries:
    @classmethod
    async def add_record(cls, fsm_data: dict):
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
        logger.info("Record added successfully")
    @classmethod
    async def get_record(cls, date) -> Record:
        async with async_session() as session:
            show_record_ = select(Record).where(cast(Record.date, Date) == date.date())
            result = await session.execute(show_record_)
            print(result)
            return result.scalar_one_or_none()

    @classmethod
    async def show_record(cls, date):
        record = await RecordQueries.get_record(date)
        print(record)
        logger.info("Record showing successfully")
        return record.show_record if record else None
    @classmethod
    async def delete_record(cls, date):
        async with async_session() as session:
            delete_record_ = delete(Record).where(cast(Record.date, Date) == date.date())
            await session.execute(delete_record_)
            await session.commit()
        logger.info("Record deleted successfully")
    @classmethod
    async def make_record_completed(cls, date):
        async with async_session() as session:
            stmt = update(Record).where(cast(Record.date, Date) == date.date()).values(completed=True)
            await session.execute(stmt)
            await session.commit()
        logger.info("Record completed successfully")