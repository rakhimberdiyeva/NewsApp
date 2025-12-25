import re

from pydantic import BaseModel, Field, field_validator


class CategoryBase(BaseModel):
    name: str = Field(max_length=100)
    description: str | None  = Field(max_length=512)
    slug: str= Field(max_length=255)
    seo_title: str | None  = Field(max_length=255)
    seo_description: str| None  = Field(max_length=320)

class CreateUpdateCategory(CategoryBase):
    @field_validator("slug", mode="before")
    @classmethod
    def validate_slug(cls, slug:str):
        slug = slug.strip().lower().replace(" ", "-")
        if not re.fullmatch(r"[a-z0-9-]+", slug):
            raise ValueError("Slug должен содержать только a-z, 0-9 и '-'")
        return slug

