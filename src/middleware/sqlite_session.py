from typing import Any

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import NextMiddlewareType
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class SQLiteSessionMiddleware(BaseMiddleware):
    def __init__(self, sqlite_sessionmaker: async_sessionmaker[AsyncSession]):
        super().__init__()
        self.sqlite_sessionmaker = sqlite_sessionmaker

    async def __call__(
        self,
        handler: NextMiddlewareType[TelegramObject],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with self.sqlite_sessionmaker() as sqlite_session:
            data["sqlite_session"] = sqlite_session

            return await handler(event, data)
