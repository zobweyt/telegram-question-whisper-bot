from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types.message_reaction_updated import MessageReactionUpdated
from aiogram.types.reply_parameters import ReplyParameters
from aiogram.utils.i18n import gettext as _

from src.services import AnonymousMessageService


async def handle_message_reaction(
    message_reaction: MessageReactionUpdated,
    bot: Bot,
    anonymous_message_service: AnonymousMessageService,
) -> None:
    if message_reaction.user is None:
        return

    existing_anonymous_message = await anonymous_message_service.get_anonymous_message_by_ids(
        to_user_id=message_reaction.user.id,
        to_message_id=message_reaction.message_id,
    )

    if existing_anonymous_message is None:
        return

    try:
        await bot.set_message_reaction(
            chat_id=existing_anonymous_message.from_user_id,
            message_id=existing_anonymous_message.from_message_id,
            reaction=message_reaction.new_reaction,
        )
    except TelegramBadRequest:
        await bot.send_message(
            chat_id=message_reaction.user.id,
            text=_("message_not_found"),
            reply_parameters=ReplyParameters(message_id=message_reaction.message_id),
        )
        return

    await bot.send_message(
        chat_id=message_reaction.user.id,
        text=_("reactions_updated"),
        reply_parameters=ReplyParameters(message_id=message_reaction.message_id),
    )
