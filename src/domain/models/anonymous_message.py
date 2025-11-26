from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.sqlite import SQLiteDeclarativeBase


class AnonymousMessage(SQLiteDeclarativeBase):
    to_user_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    to_message_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    from_user_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    from_message_id: Mapped[int] = mapped_column(primary_key=True, index=True)
