from sqlalchemy.ext.asyncio import AsyncSession

class BaseManager:
    def __init__(self, db: AsyncSession):
        self.db = db




