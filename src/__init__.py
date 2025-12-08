import logging.config

from src.settings import settings

logging.config.dictConfig(settings.logging.model_dump())
