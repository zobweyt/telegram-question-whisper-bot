from typing import Any

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import NextMiddlewareType
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from src.sqlite import AnonymousMessageSQLiteRepository


class AnonymousMessageSQLiteRepositoryMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: NextMiddlewareType[TelegramObject],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        sqlite_session = data.get("sqlite_session")

        if isinstance(sqlite_session, AsyncSession):
            data["anonymous_message_sqlite_repository"] = AnonymousMessageSQLiteRepository(
                sqlite_session=sqlite_session
            )

        return await handler(event, data)
