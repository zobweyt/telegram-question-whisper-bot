from aiogram_dialog import Dialog

from src.dialogs.user.windows import user_dialog_edit_url_window, user_dialog_view_url_window

user_dialog = Dialog(
    user_dialog_edit_url_window,
    user_dialog_view_url_window,
)
