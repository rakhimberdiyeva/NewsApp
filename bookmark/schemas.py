from pydantic import BaseModel


class BookmarkBase(BaseModel):
    article_id: int


class BookmarkCreate(BookmarkBase):
    pass