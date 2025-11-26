import asyncio
from contextlib import suppress

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import PRODUCTION, TEST
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart, ExceptionTypeFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.i18n import I18n
from aiogram.utils.i18n.middleware import SimpleI18nMiddleware
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent

from src.infrastructure.settings import settings
from src.infrastructure.sqlite import SQLiteAsyncSession
from src.infrastructure.telegram import BotLocalizer
from src.presentation.dialogs import anonymous_message_dialog, user_dialog
from src.presentation.handlers import (
    handle_error,
    handle_message_reaction,
    handle_reply_to_message,
    handle_send,
    handle_start,
    handle_start_deep_link,
    handle_unknown_intent,
    handle_user_shared,
)
from src.presentation.middlewares import (
    AnonymousMessageServiceMiddleware,
    CurrentUserMiddleware,
    SQLiteSessionMiddleware,
    UserServiceMiddleware,
)


async def main() -> None:
    bot = Bot(
        token=settings.telegram.bot_token,
        session=AiohttpSession(api=PRODUCTION if settings.telegram.server == "production" else TEST),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    i18n = I18n(
        path="locales",
    )

    bot_localizer = BotLocalizer(
        bot=bot,
        i18n=i18n,
    )

    if settings.telegram.bot_set_my:
        asyncio.create_task(bot_localizer.start_localization())

    storage = MemoryStorage()

    dispatcher = Dispatcher(
        storage=storage,
    )

    dispatcher.errors.register(handle_error, F.update.message)
    dispatcher.errors.register(handle_unknown_intent, ExceptionTypeFilter(UnknownIntent))

    dispatcher.include_routers(
        anonymous_message_dialog,
        user_dialog,
    )

    dispatcher.message.register(handle_send, Command("send"))
    dispatcher.message.register(handle_start_deep_link, CommandStart(deep_link=True))
    dispatcher.message.register(handle_start, CommandStart(deep_link=False))
    dispatcher.message.register(handle_user_shared, F.user_shared)
    dispatcher.message.register(handle_reply_to_message, F.reply_to_message)

    dispatcher.message_reaction.register(handle_message_reaction)

    SimpleI18nMiddleware(i18n).setup(dispatcher)

    dispatcher.update.middleware(SQLiteSessionMiddleware(SQLiteAsyncSession))
    dispatcher.update.middleware(UserServiceMiddleware())
    dispatcher.update.middleware(AnonymousMessageServiceMiddleware())
    dispatcher.update.middleware(CurrentUserMiddleware())

    setup_dialogs(dispatcher)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
