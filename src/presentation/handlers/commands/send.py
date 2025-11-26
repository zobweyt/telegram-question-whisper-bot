from aiogram.types import KeyboardButton, KeyboardButtonRequestUser, Message, ReplyKeyboardMarkup
from aiogram.utils.i18n import gettext as _


async def handle_send(message: Message) -> None:
    await message.answer(
        text=_("send.message.text"),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text=_("send.keyboard.request.text"),
                        request_user=KeyboardButtonRequestUser(
                            request_id=1,
                            user_is_bot=False,
                            user_is_premium=None,
                        ),
                    ),
                ],
            ],
            resize_keyboard=True,
            is_persistent=False,
        ),
    )
