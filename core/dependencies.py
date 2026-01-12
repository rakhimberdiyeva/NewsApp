from core.session import async_session


async def get_db():

        try:
            async with async_session() as session:
                yield session
        finally:
            await session.close()
