from sqlalchemy import Boolean, String, Column
from sqlalchemy.orm import relationship

from .base import BaseModel


class User(BaseModel):
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    posts = relationship("Post", back_populates="author")
