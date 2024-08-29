from pydantic import BaseModel, EmailStr


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


class TokenData(BaseModel):
    email: str | None = None


class SUserLogin(BaseModel):
    email: EmailStr
    password: str


class SUserCreate(SUserLogin):
    username: str


class SUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    disabled: bool | None = None
    is_verified: bool | None = None


class SUserInDB(SUser):
    hashed_password: str
