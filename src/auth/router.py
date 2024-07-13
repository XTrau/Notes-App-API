from datetime import timedelta

from fastapi import APIRouter, Depends, Response
from starlette import status

from auth.schemas import SUserCreate, Token, SUser
from auth.auth import authenticate_user, create_access_token, get_current_active_user, register_user
from config import settings

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register')
async def register(user: SUserCreate = Depends()):
    user = await register_user(user)
    return {"registered": True}
    # TODO: email verify


@router.post('/login')
async def login_user(response: Response, user_data: SUserCreate = Depends()):
    user = await authenticate_user(user_data.username, user_data.password)
    access_token = create_access_token(data={"sub": {"username": user.username}})
    response.set_cookie(
        key=settings.TOKEN_NAME,
        value=access_token,
        expires=timedelta(minutes=settings.TOKEN_EXPIRE_TIME + 30),
        httponly=True
    )
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie(key=settings.TOKEN_NAME)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get('/me', response_model=SUser)
async def get_account(user: SUser = Depends(get_current_active_user)):
    return user
