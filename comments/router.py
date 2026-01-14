from fastapi import APIRouter, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from article.dependencies import get_article_or_404
from article.models import Article
from auth.dependencies import get_current_user
from auth.models import User
from comments.dependencies import get_comment_or_404
from comments.models import Comment
from comments.schemas import CommentRead, CommentCreate
from comments.services import get_comment, get_comments, create_comment, delete_comment
from core.dependencies import get_db

router = APIRouter(
    prefix="/{article_id}/comments",
    # prefix="articles/{article_id}/comments",
    tags=["comment"]
)


@router.get(
    "/{comment_id}",
    status_code=200,
    response_model=CommentRead,
    summary="получение комментария по ид",
    responses={
        404: {
            "description": "комментарий не найдена"
        }
    }
)
async def get_comment_by_id(
        comment_id: int = Path(ge=1),
        session: AsyncSession = Depends(get_db)
):
    """
    **эндпоинт для получения комментария по ид**
    """
    response = await get_comment(session, comment_id)
    return response


@router.get(
    "/",
    status_code=200,
    summary="получение всех комментариев"
)
async def get_all(
        article: Article = Depends(get_article_or_404),
        session: AsyncSession = Depends(get_db),
):
    """
    **эндпоинт для получения всех комментариев**
    """
    response = await get_comments(session, article.id)
    return response


@router.post(
    "/",
    status_code=201,
    response_model=CommentRead,
    summary="создание комментария",
    responses={
        403: {
            "description": "нет прав"
        },
        404: {
            "description": "комментарий не найден"
        }
    }
    )
async def create(
        request: CommentCreate,
        user: User = Depends(get_current_user),
        article: Article = Depends(get_article_or_404),
        session: AsyncSession = Depends(get_db)
):
    """
    **эндпоинт создания комментария**
    """
    response = await create_comment(session, request, user.id, article.id)
    return response




@router.delete(
    "/",
    status_code=204,
    summary="удаление комментария",
    responses={
        403: {
            "description": "нет прав"
        },
        404: {
            "description": "комментарий не найден"
        }
    },
    )
async def delete(
        session: AsyncSession = Depends(get_db),
        comment: Comment = Depends(get_comment_or_404),
        user: User = Depends(get_current_user),
):
    """
    **эндпоинт удаления комментария**
    """
    response = await delete_comment(session=session, comment=comment, user_id=user.id)
