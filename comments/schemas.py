from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    body: str = Field(max_length=2048)


class CommentCreate(CommentBase):
    pass


class CommentRead(CommentBase):
    id: int
    user_id: int
