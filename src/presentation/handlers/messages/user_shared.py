from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _
from aiogram_dialog.api.entities.modes import ShowMode, StartMode
from aiogram_dialog.api.protocols.manager import DialogManager

from src.presentation.dialogs.anonymous_message import (
    AnonymousMessageDialogStartData,
    AnonymousMessageDialogStatesGroup,
)


async def handle_user_shared(message: Message, bot: Bot, dialog_manager: DialogManager) -> None:
    if not message.user_shared or not message.from_user:
        return

    if message.from_user.id == message.user_shared.user_id:
        await message.answer(_("start_deep_link.error.self"))
        return

    try:
        await bot.get_chat(chat_id=message.user_shared.user_id)
    except TelegramBadRequest:
        await message.reply(
            text=_("user_shared.fail"),
            reply_markup=ReplyKeyboardRemove(),
        )
        return

    await message.reply(
        text=_("user_shared.accepted"),
        reply_markup=ReplyKeyboardRemove(),
    )

    await dialog_manager.start(
        state=AnonymousMessageDialogStatesGroup.INPUT,
        data=AnonymousMessageDialogStartData(
            to_user_id=message.user_shared.user_id,
            from_user_id=message.from_user.id,
        ).model_dump(),
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )
