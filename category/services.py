from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from category.filters import CategoryFilter
from category.models import Category
from category.schemes import CategoryCreate, CategoryUpdate


async def create_category(session: AsyncSession, request: CategoryCreate) -> Category:
    category = Category(
        **request.model_dump()
    )
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


async def get_category(session: AsyncSession, category_id: int) -> Category:
    stmt = select(Category).where(Category.id == category_id)
    result = await session.execute(stmt)
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category with id {category_id} not found")
    return category



async def update_category(session: AsyncSession, category: Category, request: CategoryUpdate) -> None:
    category.name = request.name
    category.description = request.description

    session.add(category)
    await session.commit()



async def delete_category(session: AsyncSession, category: Category,) -> None:
    await session.delete(category)
    await session.commit()


async def get_categories(session: AsyncSession, filters: CategoryFilter) -> list[Category]:
    stmt = select(Category)
    stmt = filters.filter(stmt)
    stmt = filters.sort(stmt)
    result = await session.execute(stmt)
    categories = result.scalars().all()
    return categories
