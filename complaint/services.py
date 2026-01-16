from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from article.dependencies import get_article_or_404
from article.services import get_article
from comments.dependencies import get_comment_or_404
from comments.services import get_comment
from complaint.models import Complaint
from complaint.schemas import ComplaintCreate, ComplaintUpdateStatus, ComplaintStatusEnum


async def create_complaint(
        session: AsyncSession,
        request: ComplaintCreate,
        user_id: int,
) -> Complaint:
    """
    Функция для создания записи complaint в бд

    :param session: сессия бд
    :param request: Запрос с данными для создания жалобы
    :param user_id: ИД пользователя который создает жалобу
    :raise HTTPException: не найден комментарий
    :raise HTTPException: не найдена статья
    :raise HTTPException: неправильный тип
    :return: созданная жалоба
    """

    if request.target_type == "article":
        await get_article_or_404(request.target_id, session)

    elif request.target_type == "comment":
        comment = await get_comment(session, request.target_id)
        article = await get_article(session, comment.article_id)
        await get_comment_or_404(request.target_id, article, session)

    else:
        raise HTTPException(status_code=406, detail="this target type is not acceptable")


    complaint = Complaint(**request.model_dump(), user_id=user_id)
    session.add(complaint)
    await session.commit()
    await session.refresh(complaint)
    return complaint


async def get_complaints(
        session: AsyncSession
) -> list[Complaint]:
    """
    Функция для получения всех записей complaint в бд

    :param session: сессия бд
    :return: моделька жалоб
    """
    stmt = select(Complaint)
    result = await session.execute(stmt)
    complaint = result.scalars().all()
    return complaint


async def get_complaint(
        session: AsyncSession,
        complaint_id: int,
) -> Complaint:
    """
   Функция для получения записи comment в бд по ид

   :param session: сессия бд
   :param complaint_id: ИД жалобы
   :return: моделька жалобы
   """
    stmt = select(Complaint).where(Complaint.id == complaint_id)
    result = await session.execute(stmt)
    complaint = result.scalar_one_or_none()
    if not complaint:
        raise HTTPException(status_code=404, detail="complaint not found")
    return complaint


async def update_complaint(
        session: AsyncSession,
        complaint: Complaint,
        request: ComplaintUpdateStatus
) -> None:
    """
    Обновляет записи модельки жалобы

    :param session: сессия бд
    :param complaint: моделька жалобы
    :param request: Запрос с обновленными данными жалобы
    :raise HTTPException: не найдена жалоба
    :return: ничего
    """

    if request.status not in [status for status in ComplaintStatusEnum]:
        raise HTTPException(status_code=406, detail="status not acceptable")

    complaint.status = request.status
    session.add(complaint)
    await session.commit()


async def delete_complaint(
        session: AsyncSession,
        complaint: Complaint,
        user_id: int
) -> None:
    """
    Функция для удаления записи comment в бд

    :param session: сессия бд
    :param complaint: моделька жалобы
    :param user_id: ИД пользователя
    :return: ничего
    """
    if complaint.user_id != user_id:
        raise HTTPException(status_code=403, detail="you dont have permission")
    await session.delete(complaint)
    await session.commit()