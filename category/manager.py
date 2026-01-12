from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from category.models import Category
from core.manager import BaseManager


class AuthManager(BaseManager):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def create(
            self,
            name,
            description,
    ):
        stmt = insert(Category).values(
            name=name,
            description=description
        )
        await self.db.execute(stmt)
        await self.db.commit()



    async def read(
            self,
            category_id: int
    ):
        stmt = select(Category).where(Category.id == category_id)
        category = await self.db.execute(stmt)
        return category.scalar_one_or_none()


    async def list(
            self
    ):
        stmt = select(Category)
        categories = await self.db.execute(stmt)
        return categories.scalars().all()


    async def update(
            self,
            name,
            description
    ):
        stmt = update(Category).values(
            name=name,
            description=description
        )
        await self.db.execute(stmt)
        await self.db.commit()


    async def delete(
            self,
            category_id: int
    ):
        stmt = delete(Category).where(Category.id == category_id)
        category = await self.db.execute(stmt)
        return category.scalar_one_or_none()