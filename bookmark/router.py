from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from article.dependencies import get_article_or_404
from article.models import Article
from article.schemas import ArticleRead
from auth.dependencies import get_current_user
from auth.models import User
from bookmark.schemas import BookmarkCreate
from bookmark.services import add_to_bookmark, get_user_bookmark, remove_from_bookmark
from core.dependencies import get_db

router = APIRouter(
    prefix="/bookmarks",
    tags=["bookmark"],
)

@router.post(
    "/"
)
async def add_bookmark(
        request: BookmarkCreate,
        session: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    await add_to_bookmark(session, request, user.id)
    return {
        "message": "success",
    }


@router.get(
    "/",
    response_model=list[ArticleRead],
)
async def get_bookmark(
        session: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    response = await get_user_bookmark(session, user.id)
    return response


@router.delete(
    "/{article_id}",
    status_code=204,
)
async def remove_bookmark(
        article: Article = Depends(get_article_or_404),
        session: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    response = await remove_from_bookmark(session, article.id, user.id)
