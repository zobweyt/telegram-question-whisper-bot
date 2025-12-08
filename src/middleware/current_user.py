from typing import Any

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import NextMiddlewareType
from aiogram.types import TelegramObject, User

from src.services import UserService


class CurrentUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: NextMiddlewareType[TelegramObject],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user_service = data.get("user_service")
        event_from_user = data.get("event_from_user")

        if isinstance(user_service, UserService) and isinstance(event_from_user, User):
            data["current_user"] = await user_service.get_or_create_user_by_id(event_from_user.id)

        return await handler(event, data)
