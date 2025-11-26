from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.sqlite import SQLiteDeclarativeBase


class User(SQLiteDeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    url_visit_count: Mapped[int] = mapped_column(default=0)
