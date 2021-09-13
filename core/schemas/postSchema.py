from enum import Enum
from pydantic import BaseModel
from typing import Optional


class Status(str, Enum):
    active = "Active"
    inactive = "Inactive"
    suspended = "Suspended"
    deleted = "Deleted"


class BasePost(BaseModel):
    name: str
    description: str
    status: Optional[Status] = Status.active


class Post(BasePost):
    id: int
