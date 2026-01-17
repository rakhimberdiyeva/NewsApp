import os
import shutil
from pathlib import Path

from fastapi import UploadFile, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from article.models import Article
from media.models import ArticleImage

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_CONTENT_TYPES = ["image/jpeg", "image/jpg", "image/png", "image/webp"]

async def save_upload_file(
        upload_file
):
    dest = UPLOAD_DIR / upload_file.filename

    with dest.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    # return f"{UPLOAD_DIR}/{upload_file.filename}"
    return str(dest)


async def upload(
        session: AsyncSession,
        article_id: int,
        upload_file: UploadFile,
):
    if not upload_file.content_type in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Content type not allowed")

    file_path = await save_upload_file(upload_file)
    file_image = ArticleImage(
        article_id=article_id,
        filename=upload_file.filename,
        file_path=file_path,
    )
    session.add(file_image)
    await session.commit()
    return {
        "message": "success",
    }


async def download(
        session: AsyncSession,
        article: Article,
        file_id: int,
):
    stmt = select(ArticleImage).where(ArticleImage.id == file_id, ArticleImage.article_id == article.id)
    result = await session.execute(stmt)
    image = result.scalar_one_or_none()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    p = Path(image.file_path)
    if not p.exists():
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(
        path=str(p),
        filename=image.filename,
    )



async def delete(
        session: AsyncSession,
        article: Article,
        file_id: int,
):
    stmt = select(ArticleImage).where(ArticleImage.id == file_id, ArticleImage.article_id == article.id)
    result = await session.execute(stmt)
    image = result.scalar_one_or_none()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    p = Path(image.file_path)
    if not p.exists():
        raise HTTPException(status_code=404, detail="Image not found")

    await session.delete(image)

    try:
        os.remove(str(p))
    except:
        pass

    await session.commit()