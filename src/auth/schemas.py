from pydantic import BaseModel, EmailStr


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


class TokenData(BaseModel):
    email: str | None = None


class SUserBase(BaseModel):
    email: EmailStr
    username: str


class SUserCreate(SUserBase):
    password: str


class SUser(SUserBase):
    disabled: bool | None = None
    is_verified: bool | None = None


class SUserInDB(SUser):
    id: int
    hashed_password: str


class SUserLogin(BaseModel):
    login: str
    password: str
