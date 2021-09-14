from pydantic import BaseModel
from typing import Optional

from ..config.enums import Status


class BasePost(BaseModel):
    name: str
    description: str
    status: Optional[Status] = Status.published


class Post(BasePost):
    id: int

    class Config:
        orm_mode = True
