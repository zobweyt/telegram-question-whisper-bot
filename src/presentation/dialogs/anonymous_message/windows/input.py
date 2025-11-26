from aiogram import F
from aiogram.enums.content_type import ContentType
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.api.entities import ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Row, SwitchTo

from src.domain.models import AnonymousMessage
from src.domain.services import AnonymousMessageService
from src.presentation.dialogs.anonymous_message.start_data import AnonymousMessageDialogStartData
from src.presentation.dialogs.anonymous_message.state import AnonymousMessageDialogStatesGroup
from src.presentation.dialogs.format_lazy_proxy import FormatLazyProxy


async def _handle_message_input(message: Message, message_input: MessageInput, dialog_manager: DialogManager) -> None:
    if message.bot is None or not message.from_user or not isinstance(dialog_manager.start_data, dict):
        return

    start_data = AnonymousMessageDialogStartData.model_validate(dialog_manager.start_data)

    try:
        copied_message = await message.bot.copy_message(
            chat_id=start_data.to_user_id,
            from_chat_id=start_data.from_user_id,
            message_id=message.message_id,
        )
    except TelegramForbiddenError:
        await message.reply(text=_("user_blocked_bot"))
        await dialog_manager.done()
        return

    anonymous_message_service = dialog_manager.middleware_data.get("anonymous_message_service")

    if not isinstance(anonymous_message_service, AnonymousMessageService):
        return

    anonymous_message = AnonymousMessage()

    anonymous_message.to_user_id = start_data.to_user_id
    anonymous_message.to_message_id = copied_message.message_id
    anonymous_message.from_user_id = start_data.from_user_id
    anonymous_message.from_message_id = message.message_id

    await anonymous_message_service.create_anonymous_message(anonymous_message)

    dialog_manager.dialog_data["followupable"] = True

    await dialog_manager.switch_to(state=AnonymousMessageDialogStatesGroup.SENT, show_mode=ShowMode.SEND)


anonymous_message_dialog_input_window = Window(
    FormatLazyProxy(__("anonymous_message_input.message.text")),
    MessageInput(
        func=_handle_message_input,
        content_types=(ContentType.ANY,),
        filter=~CommandStart(),
    ),
    Row(
        SwitchTo(
            FormatLazyProxy(__("back")),
            id="anonymous_message_dialog_input_window_back_to_sent",
            state=AnonymousMessageDialogStatesGroup.SENT,
            when=F["dialog_data"]["followupable"],
        ),
        Cancel(FormatLazyProxy(__("cancel"))),
    ),
    state=AnonymousMessageDialogStatesGroup.INPUT,
)
