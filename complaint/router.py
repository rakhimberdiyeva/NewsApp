from fastapi import APIRouter, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_user
from auth.models import User
from complaint.dependencies import get_complaint_or_404
from complaint.models import Complaint
from complaint.schemas import ComplaintRead, ComplaintCreate, ComplaintUpdateStatus
from complaint.services import get_complaint, get_complaints, create_complaint, delete_complaint, update_complaint
from core.dependencies import get_db


router = APIRouter(
    prefix="/complaints",
    # prefix="articles/{article_id}/comments",
    tags=["complaints"]
)


@router.get(
    "/{complaint_id}",
    status_code=200,
    response_model=ComplaintRead,
    summary="получение жалобы по ид",
    responses={
        404: {
            "description": "жалоба не найдена"
        }
    }
)
async def get_complaint_by_id(
        complaint_id: int = Path(ge=1),
        session: AsyncSession = Depends(get_db)
):
    """
    **эндпоинт для получения жалобы по ид**
    """
    response = await get_complaint(session, complaint_id)
    return response


@router.get(
    "/",
    status_code=200,
    summary="получение всех жалоб"
)
async def get_all(
        session: AsyncSession = Depends(get_db),
):
    """
    **эндпоинт для получения всех жалоб**
    """
    response = await get_complaints(session)
    return response


@router.post(
    "/",
    status_code=201,
    response_model=ComplaintRead,
    summary="создание жалобы",
    responses={
        403: {
            "description": "нет прав"
        },
        404: {
            "description": "жалоба не найдена"
        }
    }
    )
async def create(
        request: ComplaintCreate,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_db)
):
    """
    **эндпоинт создания жалобы**
    """
    response = await create_complaint(session, request, user.id)
    return response


@router.patch(
    "/{complaint_id}",
    status_code=204,
    summary="частичное обновление  жалобы",
    responses={
        401: {
            "description": "не авторизован"
        },
        403: {
            "description": "нет прав"
        },
        404: {
            "description": "жалоба не найдена"
        }
    },
    )
async def update_status(
        request: ComplaintUpdateStatus,
        session: AsyncSession = Depends(get_db),
        complaint: Complaint = Depends(get_complaint_or_404)
):
    """
    **эндпоинт частичного изменения жалобы**
    """
    response = await update_complaint(session=session, complaint=complaint, request=request)


@router.delete(
    "/",
    status_code=204,
    summary="удаление жалоб",
    responses={
        403: {
            "description": "нет прав"
        },
        404: {
            "description": "жалоба не найден"
        }
    },
    )
async def delete(
        session: AsyncSession = Depends(get_db),
        complaint: Complaint = Depends(get_complaint_or_404),
        user: User = Depends(get_current_user),
):
    """
    **эндпоинт удаления жалобы**
    """
    response = await delete_complaint(session=session, complaint=complaint, user_id=user.id)
