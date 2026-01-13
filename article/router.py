from fastapi import APIRouter, Depends, Path
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from article.dependencies import is_author, is_owner, get_article_or_404
from article.filters import ArticleFilter
from article.models import Article
from article.schemas import ArticleCreate, ArticleRead, ArticleUpdate, ArticleStatusUpdate
from article.services import create_article, update_article, get_articles, get_article, delete_article
from auth.models import User
from core.dependencies import get_db

router = APIRouter(
    prefix="/articles",
    tags=["article"]
)

@router.get(
    "/{article_id}",
    status_code=200,
    response_model=ArticleRead,
    summary="получение статьи по ид",
    responses={
        404: {
            "description": "статья не найдена"
        }
    }
)
async def get_article_by_id(
        article_id: int = Path(ge=1),
        session: AsyncSession = Depends(get_db)
):
    """
    **эндпоинт для получения статьи по ид**
    """
    response = await get_article(session, article_id)
    return response


@router.get(
    "/",
    status_code=200,
    summary="получение всех статей"
)
async def get_all(
        session: AsyncSession = Depends(get_db),
        filters: ArticleFilter = FilterDepends(ArticleFilter)
):
    """
    **эндпоинт для получения всех статей**
    """
    response = await get_articles(session, filters)
    return response


@router.post(
    "/",
    status_code=201,
    response_model=ArticleRead,
    summary="создание статьи",
    responses={
        401: {
            "description": "не авторизован"
        },
        403: {
            "description": "нет прав"
        },
        404: {
            "description": "категория не найдена"
        }
    }
    )
async def create(
        request: ArticleCreate,
        user: User = Depends(is_author),
        session: AsyncSession = Depends(get_db)
):
    """
    **эндпоинт создания статьи**
    требует авторизованного пользователя с ролью автор или админ
    """
    response = await create_article(session, request, user.id)
    return response




@router.put(
    "/{article_id}",
    status_code=204,
    summary="обновление статьи",
    responses={
        401: {
            "description": "не авторизован"
        },
        403: {
            "description": "нет прав"
        },
        404: {
            "description": "статья не найдена"
        }
    },
    dependencies=[Depends(is_owner)],
    )
async def update(
        request: ArticleUpdate,
        session: AsyncSession = Depends(get_db),
        article: Article = Depends(get_article_or_404)
):
    """
    **эндпоинт обновления статьи**
    требует авторизованного пользователя с ролью автор или админ
    """
    response = await update_article(session=session, article=article, request=request)



@router.patch(
    "/{article_id}",
    status_code=204,
    summary="частичное обновление статьи",
    responses={
        401: {
            "description": "не авторизован"
        },
        403: {
            "description": "нет прав"
        },
        404: {
            "description": "статья не найдена"
        }
    },
    dependencies=[Depends(is_owner)],
    )
async def update_status(
        request: ArticleStatusUpdate,
        session: AsyncSession = Depends(get_db),
        article: Article = Depends(get_article_or_404)
):
    """
    **эндпоинт частичного изменения статьи**
    требует авторизованного пользователя с ролью автор или админ
    """
    response = await update_article(session=session, article=article, request=request)


@router.delete(
    "/{article_id}",
    status_code=204,
    summary="удаление статьи",
    responses={
        401: {
            "description": "не авторизован"
        },
        403: {
            "description": "нет прав"
        },
        404: {
            "description": "статья не найдена"
        }
    },
    dependencies=[Depends(is_owner)],
    )
async def delete(
        session: AsyncSession = Depends(get_db),
        article: Article = Depends(get_article_or_404)
):
    """
    **эндпоинт удаления статьи**
    требует авторизованного пользователя с ролью автор или админ
    """
    response = await delete_article(session=session, article=article)