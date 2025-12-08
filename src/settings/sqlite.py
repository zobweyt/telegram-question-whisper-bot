from pydantic import BaseModel


class SQLiteSettings(BaseModel):
    url: str
