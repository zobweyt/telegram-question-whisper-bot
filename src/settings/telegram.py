from typing import Literal

from pydantic.main import BaseModel


class TelegramSettings(BaseModel):
    server: Literal["production", "test"]
    bot_token: str
    bot_set_my: bool
