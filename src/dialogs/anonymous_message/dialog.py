from aiogram_dialog import Dialog

from src.dialogs.anonymous_message.windows import (
    anonymous_message_dialog_input_window,
    anonymous_message_dialog_sent_window,
)

anonymous_message_dialog = Dialog(
    anonymous_message_dialog_input_window,
    anonymous_message_dialog_sent_window,
)
