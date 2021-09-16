from sqlalchemy import Column, Enum, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from .base import BaseModel
from ..config.enums import Status


class Post(BaseModel):
    title = Column(String)
    description = Column(String)
    status = Column(Enum(Status))
    author_id = Column(Integer, ForeignKey("user.id"))

    author = relationship("User", back_populates="posts")
