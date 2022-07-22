from functools import lru_cache

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from .config import get_current_settings


@lru_cache()
def _get_engine():
    settings = get_current_settings()
    return create_async_engine(
        f"sqlite+aiosqlite:///{settings.db_filename}", echo=True, future=True
    )


async def init_db():
    engine = _get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    engine = _get_engine()
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
