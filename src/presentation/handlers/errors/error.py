from logging import getLogger

from aiogram.types import CallbackQuery, ErrorEvent, Message
from aiogram.utils.formatting import Pre, Text, as_line
from aiogram.utils.i18n import gettext as _

_logger = getLogger(__name__)


async def handle_error(event: ErrorEvent) -> None:
    _logger.error("An unexpected exception occurred:\n%s", event.exception, exc_info=True)

    if event.update.callback_query:
        await _handle_error_callback_query(event, event.update.callback_query)
    elif event.update.message:
        await _handle_error_message(event, event.update.message)


async def _handle_error_callback_query(event: ErrorEvent, callback_query: CallbackQuery) -> None:
    await callback_query.answer(_format_error_as_text(event).as_html())


async def _handle_error_message(event: ErrorEvent, message: Message) -> None:
    await message.answer(_format_error_as_text(event).as_html())


def _format_error_as_text(event: ErrorEvent) -> Text:
    return as_line(
        _("error"),
        Pre(str(event.exception)),
        sep="\n\n",
    )
