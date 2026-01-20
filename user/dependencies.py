from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_user
from auth.models import User
from auth.schemas import RoleEnum
from core.dependencies import get_db
from user.services import get_user


async def get_user_or_404(
        user_id: int,
        session: AsyncSession = Depends(get_db)
)-> User:
    """
    функция на наличие user по ид

    :param user_id: ид пользователя
    :param session: зависимость сессии бд
    :raise HTTPException: пользователь не найден
    :return: моделька пользователя
   """
    return await get_user(session=session, user_id=user_id)


async def is_admin(
        user: User = Depends(get_current_user),
) -> User:
    """
    функция для проверки роли админа

    :param user: зависимость авторизованного текущего пользователя
    :raise HTTPException: недостаточно прав
    :return: моделька пользователя
   """
    if user.role != RoleEnum.admin.value:
        raise HTTPException(
            status_code=403,
            detail="you dont have permission",
        )
    return user