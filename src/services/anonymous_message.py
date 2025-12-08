from src.sqlite import AnonymousMessage, AnonymousMessageSQLiteRepository


class AnonymousMessageService:
    def __init__(self, *, anonymous_message_sqlite_repository: AnonymousMessageSQLiteRepository):
        self.anonymous_message_sqlite_repository = anonymous_message_sqlite_repository

    async def get_anonymous_message_by_ids(self, *, to_user_id: int, to_message_id: int) -> AnonymousMessage | None:
        return await self.anonymous_message_sqlite_repository.get_by_ids(
            to_user_id=to_user_id,
            to_message_id=to_message_id,
        )

    async def create_anonymous_message(self, anonymous_message: AnonymousMessage) -> AnonymousMessage:
        return await self.anonymous_message_sqlite_repository.create(anonymous_message)
