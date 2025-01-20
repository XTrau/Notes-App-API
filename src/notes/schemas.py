from pydantic import BaseModel
from auth.schemas import SUser


class SNoteBase(BaseModel):
    title: str
    content: str


class SNoteCreate(SNoteBase):
    pass


class SNoteInDB(SNoteBase):
    id: int


class SNoteUser(SNoteInDB):
    user: SUser


class SNotePatch(BaseModel):
    title: str | None = None
    content: str | None = None
