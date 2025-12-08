from typing import Any

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import NextMiddlewareType
from aiogram.types import TelegramObject

from src.services import AnonymousMessageService
from src.sqlite import AnonymousMessageSQLiteRepository


class AnonymousMessageServiceMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: NextMiddlewareType[TelegramObject],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        anonymous_message_sqlite_repository = data.get("anonymous_message_sqlite_repository")

        if isinstance(anonymous_message_sqlite_repository, AnonymousMessageSQLiteRepository):
            data["anonymous_message_service"] = AnonymousMessageService(
                anonymous_message_sqlite_repository=anonymous_message_sqlite_repository,
            )

        return await handler(event, data)
