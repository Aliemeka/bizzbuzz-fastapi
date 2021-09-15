from sqlalchemy import String, Integer, Enum, Column

from .base import BaseModel
from ..config.enums import Status


class PostModel(BaseModel):
    __tablename__ = "posts"
    
    title = Column(String)
    description = Column(String)
    status = Column(Enum(Status))
