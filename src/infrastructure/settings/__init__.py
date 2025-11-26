from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_settings_logging import LoggingSettings

from src.infrastructure.settings.sqlite import SQLiteSettings
from src.infrastructure.settings.telegram import TelegramSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        str_strip_whitespace=True,
        ignored_types=(LoggingSettings,),
        env_file=".env",
        env_nested_delimiter="_",
        env_nested_max_split=1,
        extra="forbid",
    )

    sqlite: SQLiteSettings = Field(init=False)
    telegram: TelegramSettings = Field(init=False)

    logging = LoggingSettings()


settings = Settings()
