from typing import Any

from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.api.entities.modes import ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.link_preview import LinkPreview

from src.domain.models import User
from src.domain.services import UserService
from src.domain.validators import validate_user_url
from src.presentation.dialogs.format_lazy_proxy import FormatLazyProxy
from src.presentation.dialogs.user.state import UserDialogStatesGroup
from src.presentation.dialogs.user.url import strip_url_scheme


async def _handle_success(message: Message, dialog: Any, dialog_manager: DialogManager, new_url: str) -> None:
    user_service = dialog_manager.middleware_data.get("user_service")
    current_user = dialog_manager.middleware_data.get("current_user")

    if not isinstance(user_service, UserService) or not isinstance(current_user, User):
        return

    existing_user = await user_service.get_user_by_url(new_url)

    if existing_user is not None:
        await message.reply(_("url_busy"))
        return

    await user_service.update_user_url(current_user, url=new_url)
    await message.delete()

    await dialog_manager.switch_to(UserDialogStatesGroup.VIEW_URL, show_mode=ShowMode.EDIT)


async def _handle_error(message: Message, dialog: Any, dialog_manager: DialogManager, error: ValueError) -> None:
    await message.answer(_("url_invalid_format"))


async def _get_window_context(
    dialog_manager: DialogManager,
    current_user: User,
    **kwargs: dict[str, Any],
) -> dict[Any, Any]:
    if dialog_manager.event.bot is None:
        return {}

    start_link = await create_start_link(dialog_manager.event.bot, current_user.url)
    start_link = strip_url_scheme(start_link)

    raw_start_link = await create_start_link(dialog_manager.event.bot, "")
    raw_start_link = strip_url_scheme(raw_start_link)

    return {
        "start_link": start_link,
        "raw_start_link": raw_start_link,
    }


user_dialog_edit_url_window = Window(
    FormatLazyProxy(__("start.edit_url.text")),
    TextInput(
        id="user_dialog_edit_url_window_text_input",
        type_factory=validate_user_url,
        on_success=_handle_success,
        on_error=_handle_error,
    ),
    SwitchTo(
        text=FormatLazyProxy(__("back")),
        id="user_dialog_edit_url_window_back",
        state=UserDialogStatesGroup.VIEW_URL,
    ),
    LinkPreview(is_disabled=True),
    state=UserDialogStatesGroup.EDIT_URL,
    getter=_get_window_context,
)
