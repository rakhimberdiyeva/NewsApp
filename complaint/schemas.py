from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ComplaintStatusEnum(str, Enum):
    new = 'new'
    inProgress = 'inProgress'
    closed = 'closed'


class ComplaintBase(BaseModel):
    target_type: str = Field(max_length=20)
    target_id: int
    reason: str = Field(min_length=3)


class ComplaintCreate(ComplaintBase):
    pass


class ComplaintUpdateStatus(BaseModel):
    status: str = Field(max_length=100)


class ComplaintRead(ComplaintBase):
    id: int
    created_at: datetime
    user_id: int
    status: str = Field(max_length=100)
