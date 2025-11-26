__all__ = [
    "AnonymousMessage",
    "User",
]

import logging.config

from src.domain.models import AnonymousMessage, User
from src.infrastructure.settings import settings

logging.config.dictConfig(settings.logging.model_dump())
