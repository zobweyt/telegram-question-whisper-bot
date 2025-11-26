from aiogram.filters import CommandObject
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram_dialog import DialogManager, ShowMode, StartMode

from src.domain.services import UserService
from src.presentation.dialogs.anonymous_message import (
    AnonymousMessageDialogStartData,
    AnonymousMessageDialogStatesGroup,
)
from src.presentation.dialogs.user import UserDialogStatesGroup


async def handle_start(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        state=UserDialogStatesGroup.VIEW_URL,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )


async def handle_start_deep_link(
    message: Message,
    command: CommandObject,
    dialog_manager: DialogManager,
    user_service: UserService,
) -> None:
    if message.from_user is None or command.args is None:
        return

    to_user = await user_service.get_user_by_url(command.args)

    if to_user is None:
        await message.answer(_("start_deep_link.error.decode"))
        return

    if message.from_user.id == to_user.id:
        await message.answer(_("start_deep_link.error.self"))
        return

    await user_service.increment_user_url_visit_count_by_id(to_user.id)

    await dialog_manager.start(
        state=AnonymousMessageDialogStatesGroup.INPUT,
        data=AnonymousMessageDialogStartData(
            to_user_id=to_user.id,
            from_user_id=message.from_user.id,
        ).model_dump(),
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )
