from datetime import timedelta

from fastapi import APIRouter, Depends, Response
from starlette import status

from auth.schemas import SUserCreate, Token, SUser, SUserLogin
from auth.auth import authenticate_user, create_access_token, get_current_active_user, register_user
from config import settings

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user: SUserCreate):
    user = await register_user(user)
    return {"message": "Successfully registered"}
    # TODO: email verify


@router.post('/login')
async def login_user(response: Response, user_data: SUserLogin):
    user = await authenticate_user(user_data.email, user_data.password)
    access_token = create_access_token(data={"sub": {"email": user.email}})
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
