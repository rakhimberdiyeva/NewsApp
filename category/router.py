from fastapi import APIRouter, Depends, Path
from fastapi_filter import FilterDepends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_user
from category.dependencies import get_category_or_404
from category.filters import CategoryFilter
from category.models import Category
from category.schemes import CategoryCreate, CategoryUpdate
from category.services import create_category, update_category, delete_category, get_category, get_categories
from core.dependencies import get_db

router = APIRouter(
    prefix="/categories",
    tags=["category"]
)

@router.post("/")
async def create(request: CategoryCreate, session: AsyncSession = Depends(get_db)):
    response = await create_category(session, request)
    return response


@router.put("/{category_id}")
async def update(request: CategoryUpdate, category: Category = Depends(get_category_or_404), session: AsyncSession = Depends(get_db)):
    await update_category(session, category, request)
    return {"message": "success"}


@router.delete("/{category_id}")
async def delete(category: Category = Depends(get_category_or_404), session: AsyncSession = Depends(get_db)):
    await delete_category(session, category)
    return {"message": "success"}


@router.get("/{category_id}")
async def get_by_id(category_id: int = Path(ge=1), session: AsyncSession = Depends(get_db)):
    response = await get_category(session, category_id)
    return response

@router.get("/")
async def get_all(session: AsyncSession = Depends(get_db), filters: CategoryFilter = FilterDepends(CategoryFilter)):
    response = await get_categories(session, filters)
    return response