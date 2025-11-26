from logging import getLogger

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, ErrorEvent, Message, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _

_logger = getLogger(__name__)


async def handle_unknown_intent(event: ErrorEvent) -> None:
    _logger.warning("Restarting dialog:\n%s", event.exception)

    if event.update.callback_query:
        await _handle_unknown_intent_callback_query(event.update.callback_query)
    elif event.update.message:
        await _handle_unknown_intent_message(event.update.message)


async def _handle_unknown_intent_callback_query(callback_query: CallbackQuery) -> None:
    await callback_query.answer(_("restarted"))

    if not isinstance(callback_query.message, Message):
        return

    try:
        await callback_query.message.delete()
    except TelegramBadRequest:
        pass


async def _handle_unknown_intent_message(message: Message) -> None:
    await message.answer(_("restarted"), reply_markup=ReplyKeyboardRemove())
