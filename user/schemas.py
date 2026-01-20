from pydantic import BaseModel, Field


class UserRoleUpdate(BaseModel):
    role: str = Field(max_length=20)


class UserActivityUpdate(BaseModel):
    is_active: bool
