from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from article.dependencies import get_article_or_404
from article.models import Article
from comments.models import Comment
from comments.services import get_comment
from core.dependencies import get_db


async def get_comment_or_404(
        comment_id: int,
        article: Article = Depends(get_article_or_404),
        session: AsyncSession = Depends(get_db),
) -> Comment:
    """
    функция зависимости комментариев

    :param comment_id:ид комментария
    :param article: моделька статьи
    :param session: сессия бд
    :raise HTTPException: комментарий не найден
    :return: моделька комментария
    """
    comment = await get_comment(session=session, comment_id=comment_id)
    if comment.article_id != article.id:
        raise HTTPException(status_code=404, detail="article not found")
    return comment

