from pydantic import BaseModel

from auth.schemas import SUser


class SNoteBase(BaseModel):
    title: str
    content: str


class SNoteCreate(SNoteBase):
    user_id: int


class SNote(SNoteBase):
    id: int

class SNoteRel(SNote):
    user: SUser
