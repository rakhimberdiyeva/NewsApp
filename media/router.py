from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from article.dependencies import get_article_or_404
from article.models import Article
from core.dependencies import get_db
from media.services import upload, download, delete

router = APIRouter(
    prefix="/{article_id}/images",
)

@router.post(
    "/"
)
async def upload_image(
        file: UploadFile = File(...),
        article: Article = Depends(get_article_or_404),
        session: AsyncSession = Depends(get_db)
):
    response = await upload(session, article.id, file)
    return response


@router.get("/{file_id}")
async def download_file(
        file_id: int,
        session: AsyncSession = Depends(get_db),
        article: Article = Depends(get_article_or_404),
):
    response = await download(session, article, file_id)
    return response


@router.delete("/{file_id}")
async def delete_file(
        file_id: int,
        session: AsyncSession = Depends(get_db),
        article: Article = Depends(get_article_or_404),
):
    response = await delete(session, article, file_id)
    return response
