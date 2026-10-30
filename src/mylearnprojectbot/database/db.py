from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from mylearnprojectbot.config import settings

class Base(DeclarativeBase):
    pass

engine = create_async_engine(settings.DATABASE_URL.get_secret_value(), echo=True)
async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)