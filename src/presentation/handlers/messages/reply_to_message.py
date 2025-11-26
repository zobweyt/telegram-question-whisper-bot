from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types.message import Message
from aiogram.types.reply_parameters import ReplyParameters
from aiogram.utils.i18n import gettext as _

from src.domain.models import AnonymousMessage
from src.domain.services import AnonymousMessageService


async def handle_reply_to_message(
    message: Message,
    bot: Bot,
    anonymous_message_service: AnonymousMessageService,
) -> None:
    if message.from_user is None or message.reply_to_message is None:
        return

    existing_anonymous_message = await anonymous_message_service.get_anonymous_message(
        to_user_id=message.from_user.id,
        to_message_id=message.reply_to_message.message_id,
    )

    if existing_anonymous_message is None:
        return

    try:
        try:
            copied_message = await bot.copy_message(
                chat_id=existing_anonymous_message.from_user_id,
                message_id=message.message_id,
                from_chat_id=message.from_user.id,
                reply_parameters=ReplyParameters(message_id=existing_anonymous_message.from_message_id),
            )
        except TelegramBadRequest:
            copied_message = await bot.copy_message(
                chat_id=existing_anonymous_message.from_user_id,
                message_id=message.message_id,
                from_chat_id=message.from_user.id,
            )
    except TelegramForbiddenError:
        await message.reply(text=_("user_blocked_bot"))
        return

    new_anonymous_message = AnonymousMessage()

    new_anonymous_message.to_user_id = existing_anonymous_message.from_user_id
    new_anonymous_message.to_message_id = copied_message.message_id
    new_anonymous_message.from_user_id = message.from_user.id
    new_anonymous_message.from_message_id = message.message_id

    await anonymous_message_service.create_anonymous_message(new_anonymous_message)

    await message.reply(text=_("sent"))
