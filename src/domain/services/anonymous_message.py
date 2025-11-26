from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.anonymous_message import AnonymousMessage


class AnonymousMessageService:
    def __init__(self, *, sqlite_session: AsyncSession):
        self.sqlite_session = sqlite_session

    async def get_anonymous_message(self, *, to_user_id: int, to_message_id: int) -> AnonymousMessage | None:
        statement = select(AnonymousMessage).where(
            AnonymousMessage.to_user_id == to_user_id,
            AnonymousMessage.to_message_id == to_message_id,
        )

        result = await self.sqlite_session.execute(statement)

        return result.scalar_one_or_none()

    async def create_anonymous_message(self, anonymous_message: AnonymousMessage) -> AnonymousMessage:
        self.sqlite_session.add(anonymous_message)

        await self.sqlite_session.commit()
        await self.sqlite_session.refresh(anonymous_message)

        return anonymous_message
