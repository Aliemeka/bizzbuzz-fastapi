from sqlalchemy import String, Integer, Enum, Column

from ..config.database import Base
from ..config.enums import Status


class PostModel(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(Enum(Status))
