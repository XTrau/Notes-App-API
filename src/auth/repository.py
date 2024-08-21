from sqlalchemy import select

from auth.models import UserOrm
from auth.schemas import SUserCreate
from database import new_session


class UserRepository:
    @staticmethod
    async def get_user_by_username(username):
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.username == username)
            result = await session.execute(query)
            user = result.scalar()
            return user

    @staticmethod
    async def get_user_by_email(email: str):
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.email == email)
            result = await session.execute(query)
            user = result.scalar()
            return user

    @staticmethod
    async def create_user(user: SUserCreate, hashed_password: str):
        async with new_session() as session:
            user = UserOrm(username=user.username, email=user.email, hashed_password=hashed_password)
            session.add(user)
            await session.commit()
