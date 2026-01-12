from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from article.models import Article
from article.schemas import ArticleCreate, ArticleUpdate, ArticleStatusEnum, ArticleStatusUpdate
from category.dependencies import get_category_or_404


async def create_article(
        session: AsyncSession,
        request: ArticleCreate,
        author_id: int

) -> Article:
    """
    Функция для создания записи article в бд

    :param session: сессия бд
    :param request: Запрос с данными для создания статьи
    :param author_id: ИД пользователя который создает статью
    :raise HTTPException: не найдена категория
    :return: созданная статья
    """

    await get_category_or_404(request.category_id, session)
    article = Article(**request.model_dump(), author_id=author_id)
    session.add(article)
    await session.commit()
    await session.refresh(article)
    return article


async def update_article(
        session: AsyncSession,
        article: Article,
        request: ArticleUpdate | ArticleStatusUpdate
) -> None:
    """
    Обновляет записи модельки статьи

    Если статус статьи поменялся на публикованный, то указывается время публикации

    Если категория статьи поменялась, то проверяет наличие категории

    :param session: сессия бд
    :param article: моделька статьи
    :param request: Запрос с обновленными данными статьи
    :raise HTTPException: не найдена категория
    :return: ничего
    """

    if article.status != ArticleStatusEnum.published and request.status == ArticleStatusEnum.published:
      article.published_at = datetime.now()

    if article.category_id != request.category_id:
        await get_category_or_404(request.category_id, session)

    for key, value in request.model_dump().items():
        setattr(article, key, value)

    session.add(article)
    await session.commit()


async def delete_article(
        session: AsyncSession,
        article: Article,
) -> None:
    """
    Удаляет записи модельки статьи из бд

    :param session: сессия бд
    :param article: моделька статьи
    :return: ничего
    """
    await session.delete(article)
    await session.commit()


async def get_article(
        session: AsyncSession,
        article_id: int
):
    """
    возвращает статью из бд

    :param session: сессия бд
    :param article_id: ИД статьи
    :raise HTTPException: не найдена статья
    :return: моделька статьи
    """
    stmt = select(Article).where(Article.id == article_id)
    result = await session.execute(stmt)
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="article not found")
    return article


async def get_articles(session: AsyncSession):
    """
        возвращает все статьи из бд

        :param session: сессия бд
        :return: моделька статьей
        """
    stmt = select(Article)
    result = await session.execute(stmt)
    articles = result.scalars().all()
    return articles