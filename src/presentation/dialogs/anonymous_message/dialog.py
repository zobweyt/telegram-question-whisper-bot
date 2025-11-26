from aiogram_dialog import Dialog

from src.presentation.dialogs.anonymous_message.windows import (
    anonymous_message_dialog_input_window,
    anonymous_message_dialog_sent_window,
)

anonymous_message_dialog = Dialog(
    anonymous_message_dialog_input_window,
    anonymous_message_dialog_sent_window,
)
