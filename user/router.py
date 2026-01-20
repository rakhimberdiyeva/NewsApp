
from fastapi import APIRouter, Path, Depends
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from core.dependencies import get_db
from user.dependencies import get_user_or_404, is_admin
from user.filters import UserFilter
from user.schemas import UserRoleUpdate, UserActivityUpdate
from user.services import get_user, get_users, update_role, update_activity, delete_user

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get(
    "/{user_id}",
    status_code=200,
    summary="получение пользователя по ид",
    responses={
        404: {
            "description": "пользователь не найдена"
        }
    }
)
async def get_user_by_id(
        user_id: int= Path(ge=1),
        session: AsyncSession = Depends(get_db)
):
    """
    **эндпоинт получения пользователя по ид**
    """
    response = await get_user(session, user_id)
    return response


@router.get(
    "/",
    status_code=200,
    summary="получение всех пользователей",
)
async def get_all(
        session: AsyncSession = Depends(get_db),
        filters: UserFilter =  FilterDepends(UserFilter)
):
    """
    **эндпоинт получения всех пользователей**
    """
    response = await get_users(session, filters)
    return response


@router.patch(
    "/role",
    status_code=201,
    summary="изменение роли пользователя",
    responses={
        401: {
            "description": "не авторизован"
        },
        403: {
            "description": "нет прав"
        },
        404: {
            "description": "пользователь не найден"
        }
    },
    dependencies=[Depends(is_admin)]
)
async def update_user_role(
        request: UserRoleUpdate,
        session: AsyncSession = Depends(get_db),
        user: User = Depends(get_user_or_404)
):
    """
    **эндпоинт обновления роли пользователя**
    требует авторизованного пользователя с ролью админ
    """
    response = await update_role(request, session, user)
    return response



@router.patch(
    "/activity",
    status_code=201,
    summary="изменение активности пользователя",
    responses={
        401: {
            "description": "не авторизован"
        },
        403: {
            "description": "нет прав"
        },
        404: {
            "description": "пользователь не найден"
        }
    },
    dependencies=[Depends(is_admin)]
)
async def update_user_activity(
        request: UserActivityUpdate,
        session: AsyncSession = Depends(get_db),
        user: User = Depends(get_user_or_404)
):
    """
   **эндпоинт обновления активности пользователя**
   требует авторизованного пользователя с ролью админ
   """
    response = await update_activity(request, session, user)
    return response



@router.delete(
    "/",
    status_code=201,
    summary="удаление пользователя",
    responses={
        401: {
            "description": "не авторизован"
        },
        403: {
            "description": "нет прав"
        },
        404: {
            "description": "пользователь не найден"
        }
    },
    dependencies=[Depends(is_admin)]
)
async def delete(
        session: AsyncSession = Depends(get_db),
        user: User = Depends(get_user_or_404)
):
    """
   **эндпоинт удаления пользователя**
   требует авторизованного пользователя с ролью админ
   """
    response = await delete_user(session, user)
    return response