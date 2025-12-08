from typing import Any

from pydantic.alias_generators import to_snake
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase


class SQLiteDeclarativeBase(DeclarativeBase):
    @declared_attr
    @classmethod
    def __tablename__(cls) -> Any:
        return to_snake(cls.__name__)
