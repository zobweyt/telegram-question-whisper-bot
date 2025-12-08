import re
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram.utils.deep_linking import BAD_PATTERN, create_start_link
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.api.entities.modes import ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from aiogram_dialog.widgets.link_preview import LinkPreview

from src.dialogs.format_lazy_proxy import FormatLazyProxy
from src.dialogs.user.state import UserDialogStatesGroup
from src.dialogs.user.url import strip_url_scheme
from src.services import UserService
from src.sqlite import User


def _validate_user_url(url: str) -> str:
    if re.search(BAD_PATTERN, url):
        raise ValueError("User URL must contain only A-Z, a-z, 0-9, _ and -")

    if len(url) > 64:
        raise ValueError("User URL must be up to 64 characters long.")

    return url


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


async def _use_random_url(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    user_service = dialog_manager.middleware_data.get("user_service")
    current_user = dialog_manager.middleware_data.get("current_user")

    if not isinstance(user_service, UserService) or not isinstance(current_user, User):
        return

    await user_service.update_user_url(current_user, url=await user_service.generate_unique_user_url())

    await dialog_manager.switch_to(UserDialogStatesGroup.VIEW_URL, show_mode=ShowMode.EDIT)


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
        type_factory=_validate_user_url,
        on_success=_handle_success,
        on_error=_handle_error,
    ),
    Button(
        text=FormatLazyProxy(__("use_random_url")),
        id="user_dialog_edit_url_window_use_random_url",
        on_click=_use_random_url,
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
