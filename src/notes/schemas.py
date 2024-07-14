from pydantic import BaseModel

from auth.schemas import SUser


class SNote(BaseModel):
    title: str
    content: str


class SNoteCreate(SNote):
    user_id: int | None = None


class SNoteRel(SNote):
    user: SUser
