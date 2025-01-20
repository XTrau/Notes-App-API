from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, Depends, Response
from starlette import status

from auth.jwt import create_access_token, create_refresh_token
from auth.schemas import SUserCreate, SUserInDB, SUser
from auth.auth import authenticate_user, get_current_active_user, register_user
from config import settings

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user: SUserCreate):
    user = await register_user(user)
    return {"message": "Successfully registered"}
    # TODO: email verify


@router.post('/login')
async def login_user(response: Response, user: SUserInDB = Depends(authenticate_user)):
    refresh_token = create_access_token({"email": user.email})
    access_token = create_refresh_token({"email": user.email})
    response.set_cookie(
        key=settings.jwt.ACCESS_TOKEN_NAME,
        value=access_token,
        expires=datetime.now(timezone.utc) + timedelta(minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_TIME + 30),
        httponly=True
    )
    response.set_cookie(
        key=settings.jwt.REFRESH_TOKEN_NAME,
        value=refresh_token,
        expires=datetime.now(timezone.utc) + timedelta(minutes=settings.jwt.REFRESH_TOKEN_EXPIRE_TIME + 30),
        httponly=True
    )
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie(key=settings.jwt.ACCESS_TOKEN_NAME)
    response.delete_cookie(key=settings.jwt.REFRESH_TOKEN_NAME)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get('/me', response_model=SUser)
async def get_account(user: SUser = Depends(get_current_active_user)):
    return user
