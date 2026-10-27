from datetime import date

from sqlalchemy import String, Date, Boolean, false
from sqlalchemy.orm import Mapped, mapped_column

from mylearnprojectbot.database.db import Base


class Record(Base):

    __tablename__ = "record"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject: Mapped[str] = mapped_column(String, nullable=False)
    topic: Mapped[str] = mapped_column(String, nullable=False)
    ration: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, server_default=false(), default=False, nullable=False)

    @property
    def show_record(self):
        return self.subject, self.topic, self.ration, self.date, self.completed
