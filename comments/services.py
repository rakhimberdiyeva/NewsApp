from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from article.dependencies import get_article_or_404
from comments.models import Comment
from comments.schemas import CommentCreate


async def create_comment(
        session: AsyncSession,
        request: CommentCreate,
        user_id: int,
        article_id: int
) -> Comment:
    """
    Функция для создания записи comment в бд

    :param session: сессия бд
    :param request: Запрос с данными для создания комментария
    :param user_id: ИД пользователя который создает комментарий
    :param article_id: ИД статьи к которому пишется комментарий
    :raise HTTPException: не найдена статья
    :return: созданный комментарий
    """

    await get_article_or_404(article_id, session)
    comment = Comment(**request.model_dump(), user_id=user_id, article_id=article_id)
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment


async def get_comments(
        session: AsyncSession,
        article_id: int
) -> list[Comment]:
    """
    Функция для получения всех записей comment в бд

    :param session: сессия бд
    :param article_id: ИД статьи к которому написан комментарий
    :return: моделька комментариев
    """
    stmt = select(Comment).where(Comment.article_id == article_id)
    result = await session.execute(stmt)
    comments = result.scalars().all()
    return comments


async def get_comment(
        session: AsyncSession,
        comment_id: int,
) -> Comment:
    """
   Функция для получения записи comment в бд по ид

   :param session: сессия бд
   :param comment_id: ИД комментария
   :return: моделька комментария
   """
    stmt = select(Comment).where(Comment.id == comment_id)
    result = await session.execute(stmt)
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="comment not found")
    return comment


async def delete_comment(
        session: AsyncSession,
        comment: Comment,
        user_id: int
) -> None:
    """
    Функция для удаления записи comment в бд

    :param session: сессия бд
    :param comment: моделька комментария
    :param user_id: ИД пользователя
    :return: ничего
    """
    if comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="you dont have permission")
    await session.delete(comment)
    await session.commit()