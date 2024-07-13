from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class SUserCreate(BaseModel):
    username: str
    password: str
    hashed_password: str | None = None


class SUser(BaseModel):
    username: str
    email: EmailStr | None = None
    disabled: bool | None = None
    is_verified: bool | None = None


class SUserInDB(SUser):
    hashed_password: str
