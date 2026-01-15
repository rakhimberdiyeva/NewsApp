from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from complaint.models import Complaint
from complaint.services import get_complaint
from core.dependencies import get_db


async def get_complaint_or_404(
        complaint_id: int,
        session: AsyncSession = Depends(get_db)
)-> Complaint:
    """
    функция на наличие жалобы по ид

    :param complaint_id: ид жалобы
    :param session: зависимость сессии бд
    :raise HTTPException: жалоба не найдена
    :return: моделька жалобы
   """
    return await get_complaint(session=session, complaint_id=complaint_id)