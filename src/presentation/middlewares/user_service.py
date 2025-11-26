from typing import Any

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import NextMiddlewareType
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.services import UserService


class UserServiceMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: NextMiddlewareType[TelegramObject],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        sqlite_session = data.get("sqlite_session")

        if isinstance(sqlite_session, AsyncSession):
            data["user_service"] = UserService(sqlite_session=sqlite_session)

        return await handler(event, data)
