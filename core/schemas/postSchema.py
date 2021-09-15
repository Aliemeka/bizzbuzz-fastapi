from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from ..config.enums import Status


class BasePost(BaseModel):
    title: str
    description: str
    status: Optional[Status] = Status.published


class Post(BasePost):
    id: UUID

    class Config:
        orm_mode = True
