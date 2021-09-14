from enum import Enum
from pydantic import BaseModel
from typing import Optional


class Status(str, Enum):
    published = "Published"
    draft = "Draft"
    archived = "Archived"
    deleted = "Deleted"


class BasePost(BaseModel):
    name: str
    description: str
    status: Optional[Status] = Status.published


class Post(BasePost):
    id: int
