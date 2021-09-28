from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import BaseModel
from ..config.typing import GUID


class Reply(BaseModel):
    message = Column(String, nullable=False)
    post_id = Column(GUID, ForeignKey("post.id"))
    author_id = Column(GUID, ForeignKey("user.id"))

    post = relationship("Post", back_ref="replies")
    author = relationship("User", back_ref="replies")
