from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from config import settings

engine = create_async_engine(url=settings.db.database_url_asyncpg)
new_session = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session
