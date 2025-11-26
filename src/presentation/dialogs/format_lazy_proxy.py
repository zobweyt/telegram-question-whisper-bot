from typing import Any, cast

from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from babel.support import LazyProxy


class FormatLazyProxy(Text):
    def __init__(self, lazy_proxy: LazyProxy, when: WhenCondition = None):
        super().__init__(when)
        self.lazy_proxy = lazy_proxy

    async def _render_text(self, data: dict[str, Any], manager: DialogManager) -> str:
        return cast(str, self.lazy_proxy.value).format_map(data)
