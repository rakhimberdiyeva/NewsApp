from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from article.dependencies import get_article_or_404
from article.models import Article
from bookmark.models import Bookmark
from bookmark.schemas import BookmarkCreate



async def add_to_bookmark(
        session: AsyncSession,
        request: BookmarkCreate,
        user_id: int
):
    """
    Функция для создания записи bookmark в бд

    :param session: сессия бд
    :param request: Запрос с данными для создания букмарка
    :param user_id: ИД пользователя
    :raise HTTPException: не найдена статья
    :return: ничего
    """


    await get_article_or_404(request.article_id, session)
    bookmark = Bookmark(
        article_id=request.article_id,
        user_id=user_id,
    )
    session.add(bookmark)
    await session.commit()


async def remove_from_bookmark(
        session: AsyncSession,
        article_id: int,
        user_id: int
):
    """
    Функция для удаления записи bookmark в бд

    :param session: сессия бд
    :param article_id: ИД статьи
    :param user_id: ИД пользователя
    :return: ничего
    """

    stmt = delete(Bookmark).where(Bookmark.article_id == article_id, Bookmark.user_id == user_id)
    result = await session.execute(stmt)
    await session.commit()


async def get_user_bookmark(
        session: AsyncSession,
        user_id: int,
) -> list[Bookmark]:

    """
    Функция для получения всех записей bookmark в бд

    :param session: сессия бд
    :param user_id: ИД пользователя
    :return: список букмарков
    """

    stmt = select(Article).join(Bookmark).where(Bookmark.user_id == user_id)
    result = await session.execute(stmt)
    articles = result.scalars().all()
    return articles

