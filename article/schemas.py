from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ArticleStatusEnum(str, Enum):
    draft = 'draft'
    published = 'published'


class ArticleBase(BaseModel):
    title: str = Field(min_length=3, max_length=512)
    content: str = Field(min_length=10)
    category_id: int = Field(ge=1)
    status: ArticleStatusEnum


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(ArticleBase):
    pass


class ArticleStatusUpdate(BaseModel):
    category_id: int = Field(ge=1)
    status: ArticleStatusEnum


class ArticleRead(ArticleBase):
    id: int
    author_id: int
    #author
    #category
    published_at: datetime | None = None