from aiogram.utils.i18n import lazy_gettext as __
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import SwitchTo

from src.presentation.dialogs.anonymous_message.state import AnonymousMessageDialogStatesGroup
from src.presentation.dialogs.format_lazy_proxy import FormatLazyProxy

anonymous_message_dialog_sent_window = Window(
    FormatLazyProxy(__("sent")),
    SwitchTo(
        FormatLazyProxy(__("followup")),
        id="anonymous_message_dialog_sent_window_followup",
        state=AnonymousMessageDialogStatesGroup.INPUT,
    ),
    state=AnonymousMessageDialogStatesGroup.SENT,
)
