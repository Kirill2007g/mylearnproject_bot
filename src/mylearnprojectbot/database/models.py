from datetime import datetime

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Record(Base):
    __tablename__ = "record"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subject: Mapped[String] = mapped_column(String, nullable=False)
    topic: Mapped[String] = mapped_column(String, nullable=False)
    ration: Mapped[String] = mapped_column(String, nullable=False)
    completed_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
