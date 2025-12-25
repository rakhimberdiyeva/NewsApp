from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from category.models import Category
from category.schemes import CreateUpdateCategory
from core.manager import BaseManager


class AuthManager(BaseManager):
    def __init__(self, db: AsyncSession):
        super().__init__(db)


    async def create(
            self,
            request: CreateUpdateCategory
    ):

        data = request.model_dump()
        stmt = insert(Category).values(
            **data
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
            request: CreateUpdateCategory,
            category_id: int
    ):
        data = request.model_dump(exclude_unset=True)
        stmt = update(Category).values(
            **data
        ).where(Category.id == category_id)
        await self.db.execute(stmt)
        await self.db.commit()


    async def delete(
            self,
            category_id: int
    ):
        stmt = delete(Category).where(Category.id == category_id)
        await self.db.execute(stmt)
        await self.db.commit()