import urllib.parse
from typing import Any

from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.link import create_telegram_link
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import CopyText, Row, SwitchTo, Url
from aiogram_dialog.widgets.link_preview import LinkPreview
from aiogram_dialog.widgets.text import Format

from src.domain.models import User
from src.presentation.dialogs.format_lazy_proxy import FormatLazyProxy
from src.presentation.dialogs.user.state import UserDialogStatesGroup
from src.presentation.dialogs.user.url import strip_url_scheme


async def _get_window_context(
    dialog_manager: DialogManager,
    current_user: User,
    **kwargs: dict[str, Any],
) -> dict[Any, Any]:
    if dialog_manager.event.bot is None:
        return {}

    start_link = await create_start_link(dialog_manager.event.bot, current_user.url)
    start_link = strip_url_scheme(start_link)

    share_url_url = _("start.keyboard.share.url.url").format(start_link=start_link)

    path = f"/share/url?url={urllib.parse.quote(share_url_url)}"
    share_link = create_telegram_link(path)

    return {
        "start_link": start_link,
        "share_link": share_link,
        "url_visit_count": current_user.url_visit_count,
    }


user_dialog_view_url_window = Window(
    FormatLazyProxy(__("start.message.text")),
    Row(
        Url(
            text=FormatLazyProxy(__("start.keyboard.share.text")),
            url=Format("{share_link}"),
        ),
        CopyText(
            text=FormatLazyProxy(__("start.keyboard.copy.text")),
            copy_text=Format("{start_link}"),
        ),
    ),
    SwitchTo(
        text=FormatLazyProxy(__("start.keyboard.edit.text")),
        id="user_dialog_view_url_window_switch_to_edit_url",
        state=UserDialogStatesGroup.EDIT_URL,
    ),
    LinkPreview(is_disabled=True),
    state=UserDialogStatesGroup.VIEW_URL,
    getter=_get_window_context,
)
