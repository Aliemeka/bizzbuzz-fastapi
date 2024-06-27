from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from ..config.enums import Status


class BasePost(BaseModel):
    title: str
    description: str
    status: Optional[Status] = Status.published


class PostCreate(BasePost):
    pass


class Post(BasePost):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
