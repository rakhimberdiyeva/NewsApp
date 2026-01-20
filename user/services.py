from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from auth.schemas import RoleEnum
from user.filters import UserFilter
from user.schemas import UserRoleUpdate, UserActivityUpdate


async def get_user(
        session: AsyncSession,
        user_id: int
) -> User:
    """
    Функция для получения пользователя по ид

    :param session: сессия бд
    :param user_id: ИД пользователя
    :return: моделька пользователя
    """
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


async def get_users(
        session: AsyncSession,
        filters: UserFilter
) -> list[User]:
    """
    Функция для получения всех пользователей

    :param session: сессия бд
    :param filters: фильтры для поиска
    :return: список пользователей
    """
    stmt = select(User)
    stmt = filters.filter(stmt)
    result = await session.execute(stmt)
    users = result.scalars().all()
    return users


async def update_role(
        request: UserRoleUpdate,
        session: AsyncSession,
        user: User
) -> None:
    """
    Функция для обновления роли пользователя

    :param session: сессия бд
    :param user: моделька пользователя
    :param request: Запрос с данными для обновления
    :return: ничего
    """
    if request.role not in [role.value for role in RoleEnum]:
        raise HTTPException(status_code=406, detail="role not acceptable")

    user.role = request.role
    session.add(user)
    await session.commit()


async def update_activity(
        request: UserActivityUpdate,
        session: AsyncSession,
        user: User
) -> None:
    """
    Функция для обновления активности пользователя

    :param session: сессия бд
    :param user: моделька пользователя
    :param request: Запрос с данными для обновления
    :return: ничего
    """
    user.is_active = request.is_active
    session.add(user)
    await session.commit()


async def delete_user(
        session: AsyncSession,
        user: User
) -> None:
    """
    Функция для удаления пользователя из бд

    :param session: сессия бд
    :param user: моделька пользователя
    :return: ничего
    """
    await session.delete(user)
    await session.commit()