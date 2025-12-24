from core.session import async_session


async def get_db():
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
        finally:
            await session.close()
