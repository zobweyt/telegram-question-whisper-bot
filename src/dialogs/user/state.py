from aiogram.fsm.state import State, StatesGroup


class UserDialogStatesGroup(StatesGroup):
    EDIT_URL = State()
    VIEW_URL = State()
