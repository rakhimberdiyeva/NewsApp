
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine("postgresql+asyncpg://postgres:111@localhost:5432/NewsApp", echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)