from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(min_length=3, max_length=320)
    description: str = Field(max_length=2048)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int