from typing import Any

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import NextMiddlewareType
from aiogram.types import TelegramObject

from src.services import UserService
from src.sqlite import UserSQLiteRepository


class UserServiceMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: NextMiddlewareType[TelegramObject],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user_sqlite_repository = data.get("user_sqlite_repository")

        if isinstance(user_sqlite_repository, UserSQLiteRepository):
            data["user_service"] = UserService(user_sqlite_repository=user_sqlite_repository)

        return await handler(event, data)
