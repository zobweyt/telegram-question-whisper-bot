from aiogram.fsm.state import State, StatesGroup


class AnonymousMessageDialogStatesGroup(StatesGroup):
    INPUT = State()
    SENT = State()
