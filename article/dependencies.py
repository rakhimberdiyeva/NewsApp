from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from article.models import Article
from article.services import get_article
from auth.dependencies import get_current_user
from auth.models import User
from auth.schemas import RoleEnum
from core.dependencies import get_db


async def get_article_or_404(
        article_id: int,
        session: AsyncSession = Depends(get_db)
)-> Article:
    """
    функция на наличие статьи по ид

    :param article_id: ид статьи
    :param session: зависимость сессии бд
    :raise HTTPException: статья не найдена
    :return: моделька статьи
   """
    # зависит от бд
    return await get_article(session=session, article_id=article_id)



# проверка на то что пользователь автор
async def is_author(
        user: User = Depends(get_current_user),
        # article: Article = Depends(get_article_or_404)
) -> User:
    """
    функция для проверки роли автора

    :param user: зависимость авторизованного текущего пользователя
    :raise HTTPException: недостаточно прав
    :raise HTTPException: пользователь не авторизован
    :return: моделька пользователя
   """
    # зависим от того что пользователь авторизован
    if user.role not in [RoleEnum.author.value, RoleEnum.admin.value]:
        raise HTTPException(
            status_code=403,
            detail="you dont have permission to create/update article",
        )
    return user

# проверка на авторство
async def is_owner(
        user: User = Depends(is_author),
        article: Article = Depends(get_article_or_404),
) -> None:
    """
    функция для проверки владельца статьи

    :param user: зависимость пользователя с ролью автор или админ
    :param article: зависимость от статьи
    :raise HTTPException: недостаточно право
    :raise HTTPException: статья не найдена
    :return: ничего
    """
    # зависим от статьи
    # зависим от того что пользователь авторизован
    if article.author_id != user.id and user.role != RoleEnum.admin.value:
        raise HTTPException(
            status_code=403,
            detail="you dont have permission to create/update article",
        )


