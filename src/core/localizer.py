import asyncio
from logging import getLogger

from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from aiogram.utils.i18n import I18n

_logger = getLogger(__name__)


class BotLocalizer:
    def __init__(self, *, bot: Bot, i18n: I18n) -> None:
        self.bot = bot
        self.i18n = i18n

    async def start_localization(self) -> None:
        _logger.info("Starting bot localization for available locales: %s", self.i18n.available_locales)

        try:
            await asyncio.gather(*map(self.set_my, self.i18n.available_locales))

            _logger.info("Bot localization completed")
        except TelegramRetryAfter as exception:
            _logger.error(exception.message.replace("\n", " "))

    async def set_my(self, locale: str) -> None:
        _logger.debug("Starting bot localization for locale: %s", locale)

        language_code = None if locale == self.i18n.default_locale else locale

        await asyncio.gather(
            self.set_my_name(locale, language_code),
            self.set_my_description(locale, language_code),
            self.set_my_short_description(locale, language_code),
            self.set_my_commands(locale, language_code),
        )

        _logger.debug("Bot localization completed for locale: %s", locale)

    async def set_my_name(self, locale: str, language_code: str | None) -> None:
        await self.bot.set_my_name(
            self.i18n.gettext("bot.name", locale=locale),
            language_code=language_code,
        )

    async def set_my_description(self, locale: str, language_code: str | None) -> None:
        await self.bot.set_my_description(
            self.i18n.gettext("bot.description", locale=locale),
            language_code=language_code,
        )

    async def set_my_short_description(self, locale: str, language_code: str | None) -> None:
        await self.bot.set_my_short_description(
            self.i18n.gettext("bot.short_description", locale=locale),
            language_code=language_code,
        )

    async def set_my_commands(self, locale: str, language_code: str | None) -> None:
        await self.bot.set_my_commands(
            commands=[
                BotCommand(
                    command="start",
                    description=self.i18n.gettext("bot.commands.start.description", locale=locale),
                ),
                BotCommand(
                    command="send",
                    description=self.i18n.gettext("bot.commands.send.description", locale=locale),
                ),
            ],
            scope=BotCommandScopeAllPrivateChats(),
            language_code=language_code,
        )
