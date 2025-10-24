__all__ = ["AsyncSessionDep"]
from typing import Annotated, AsyncIterable
from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config import settings


# Здесь будет создан движок

engine = create_async_engine(url=settings.db.url, echo=settings.alchemy.echo)
session_maker = async_sessionmaker(engine, expire_on_commit=settings.alchemy.expire_on_commit)


async def get_async_session() -> AsyncIterable[AsyncSession]:
    async with session_maker() as session:
        yield session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
