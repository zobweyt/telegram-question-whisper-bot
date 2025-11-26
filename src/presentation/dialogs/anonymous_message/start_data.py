from pydantic import BaseModel


class AnonymousMessageDialogStartData(BaseModel):
    to_user_id: int
    from_user_id: int
