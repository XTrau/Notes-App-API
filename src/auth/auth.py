from datetime import datetime, timezone, timedelta
import jwt
from fastapi import Depends, HTTPException, Request
from jwt import InvalidTokenError
from passlib.context import CryptContext
from starlette import status

from auth.repository import UserRepository
from auth.schemas import TokenData, SUser, SUserCreate, SUserInDB
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"])


async def get_token_from_cookies(request: Request):
    token = request.cookies.get(settings.TOKEN_NAME, None)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return token


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.TOKEN_EXPIRE_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(username: str, password: str):
    user_model = await UserRepository.get_user_by_username(username=username)
    if user_model is None:
        return False
    if not verify_password(password, user_model.hashed_password):
        return False
    return SUser.model_validate(user_model, from_attributes=True)


async def get_current_user(token: str = Depends(get_token_from_cookies)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        payload_dict = payload.get("sub")
        if payload_dict is None:
            raise credentials_exception
        token_data = TokenData(username=payload_dict.get("username"))
    except InvalidTokenError:
        raise credentials_exception
    user_model = await UserRepository.get_user_by_username(username=token_data.username)
    return SUserInDB.model_validate(user_model, from_attributes=True)


async def get_current_active_user(user: SUser = Depends(get_current_user)):
    if user.disabled is True:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user


async def register_user(user: SUserCreate):
    user_model = await UserRepository.get_user_by_username(user.username)
    if user_model is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already exists",
        )
    user.hashed_password = get_password_hash(user.password)
    await UserRepository.create_user(user)
    user_model = await UserRepository.get_user_by_username(user.username)
    return SUser.model_validate(user_model, from_attributes=True)
